import os
import glob
import orgparse
import pandas as pd
import re
from config import org_roam_path, banned_org_roam_files


def get_all_files_in_folder(full=False):
    path = os.path.join(org_roam_path, "**/*.org")
    files = set(glob.glob(path, recursive=True))
    files = files.difference(set(f for f in files if any(word in f for word in banned_org_roam_files)))
    if not full:
        files = [os.path.splitext(os.path.basename(file))[0] for file in files]
    return files

def extract_org_title(node):
    if node.heading:
        return node.heading
    else:
        title_pattern = re.compile(r'^#\+title:\s*(.*)$', re.IGNORECASE)
        match = title_pattern.search(node.body)
        if match:
            return match.group(1)
        else:
            return re.sub(r"#\+title:", "", node.body.split("\n")[0], flags=re.IGNORECASE).strip()


def extract_org_nested_body(node):
    body = node.body
    for child in node.children:
        body += '\n' + child.level * "*" + " " + child.heading + "\n" + extract_org_nested_body(child)
    return body.strip()

def extract_org_nested_body_exclusive(node):
    body = node.body
    for child in node.children:
        if not child.properties.get('ID') and not child.properties.get('SEARCH'):
            body += '\n' + child.level * "*" + " " + child.heading + "\n" + extract_org_nested_body_exclusive(child)
    return body.strip()

def build_node_hierarchy(node):
    hierarchy = [extract_org_title(node)]
    parent = node.parent

    # while parent and parent != org_data[0]:
    while parent:
        hierarchy.append(extract_org_title(parent))
        parent = parent.parent
    return ' > '.join(reversed(hierarchy)).strip()

def node_to_dict(node, file_name):
    node_dict = {
        'file_name': file_name,
        'node_id': node.properties.get('ID'),
        'node_title': extract_org_title(node),
        'node_hierarchy': build_node_hierarchy(node),
        'node_text': node.body,
        'node_text_nested': extract_org_nested_body(node),
        'node_text_nested_exclusive': extract_org_nested_body_exclusive(node),
    }
    return node_dict

def org_roam_nodes_to_dataframe(org_file):
    org_data = orgparse.load(org_file)
    nodes = [node_to_dict(node, org_file) for node in org_data[0][:] if node.properties.get('ID')]
    return pd.DataFrame(nodes)

def org_roam_df():
    org_files = get_all_files_in_folder(full=True)
    df = pd.concat([org_roam_nodes_to_dataframe(org_file) for org_file in org_files])
    df["text_to_encode"] = (
        df["node_text_nested_exclusive"]
        .astype(str)
        .str.replace("#\+filetags:", "tags:")
        .str.replace("#\+title:", "title:")
        .str.replace("#\+STARTUP: inlineimages latexpreview", "")
    )
    df["text_to_encode"] = ("[" + df["node_hierarchy"] + "] " + df["text_to_encode"].astype(str))
    return df
