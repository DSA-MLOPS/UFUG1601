def get_head_contents(md_filename):
    with open(md_filename, "r") as f:
        content = f.readlines()
        
    head_contents = []
    current_content = {}
    for line in content:
        if line.startswith("# "):  # New heading found
            if current_content:  # If there's previous content, add it to the list
                head_contents.append(current_content)
            current_content = {"title": line[2:].strip(), "body": []}
        else:
            current_content["body"].append(line)
    if current_content:  # Add the last piece of content
        head_contents.append(current_content)
        
    heads = {}   
    for hc in head_contents:
        heads[hc["title"]] = {"description": " ".join(hc['body'])}
        
    return heads

if __name__ == "__main__":
    heads = get_head_contents("hw.md")
    print(heads)