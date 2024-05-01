import json
import random

def extract(filepath: str, comment_indicator: str = "#", keyword: str = "", keyword_begins: int = -1, show_line: bool = False):
    """
    Extracts data stored in comments

    Args:
        filepath (str): path to commented file
        comment_indicator (str, optional): the character(s) a comment starts with. Defaults to "#".
        keyword (str, optional): An additional string to get lines starting with such string after the #, include any special character that could hinder json parsing. Defaults to "" which indicates no preferred lines.
        keyword_begins (int, optional): A optional parameter to indicate if the keyword starts, ends or is within the comment, < 0 (starts), 0 (within) and > 0 (ends). Defaults to -1
        show_line (bool, optional): Indicates whether to show line number. Defaults to False

    Returns:
        list: List of all extracted comments
    """
    pre_extracted: list[{int, str}] = []
    filtered: list[str] = []
    
    with open(filepath, "r") as file:
        file_lines = file.readlines()
        
        for i in range(len(file_lines)):
            line = file_lines[i]
            line = line.strip().strip("\n")
            
            if(line.startswith(comment_indicator)):
                line = line.strip(comment_indicator)
                pre_extracted.append({"line_number": i+1, "line_text": line})
                        
        for ext in pre_extracted:
            line_text = ext.get("line_text")
            line_number = ext.get("line_number")
            line_indicator = f"Line {line_number}: " if show_line else ""
            text = line_text.strip()
            if(keyword):
                extracted = text.strip(keyword).strip()
                if(keyword_begins < 0):
                    if(text.startswith(keyword)):
                        filtered.append(line_indicator + extracted)
                elif(keyword_begins > 0):
                    if(text.endswith(keyword)):
                        filtered.append(line_indicator + extracted)
                else:
                    if(text.find(keyword) > -1):
                        filtered.append(line_indicator + extracted)
            else:
                filtered.append(line_indicator + text)
                
    return filtered


def extract_json(filepath: str, comment_indicator: str = "#", keyword: str = "", keyword_begins: int = -1):
    """
    This is for extracting json data primarily stored in comments, for example google forms store options in comments.
    Only works for single line comments at the moment \n
    
    ### Does not support showing line numbers. Why should it?

    Args:
        filepath (str): The path to the already generated text file in json format
        comment_indicator (str, optional): the character(s) a comment starts with. Defaults to "#".
        keyword (str, optional): An additional string to get lines starting with such string after the #, include any special character that could hinder json parsing. Defaults to "" which indicates no preferred lines.
        keyword_begins(int, optional): A optional parameter to indicate if the keyword starts, ends or is within the comment, < 0 (starts), 0 (within) and > 0 (ends). Defaults to -1

    Returns:
        list: List of extracted comments
    """
    arrays = extract(filepath, comment_indicator, keyword, keyword_begins)
    decoder = json.JSONDecoder()

    for i in range(len(arrays)):
        filt = arrays[i] 
        filt = filt.replace("['", '["').replace("']", '"]').replace("',", '",').replace(", '", ', "')
        
        try:
            decoded = decoder.decode(filt)
        except Exception as jerror:
            if(jerror):
                continue
        arrays[i] = decoded

    return arrays

if __name__ == "__main__":
    for option in extract_json("./fields.jsonc", "//", "Options:", -1):
        if isinstance(option, list):
            print(f"{random.choice(option)}\n")
        else:
            print(option)