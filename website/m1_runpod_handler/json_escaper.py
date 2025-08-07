import sys
import json

def escape_for_json(text):

    # This handles newlines, quotes, backslashes, and other JSON special characters.
    
    # Use json.dumps to properly escape the string, then remove the surrounding quotes
    escaped = json.dumps(text)[1:-1]
    return escaped

def main():
    print("JSON Text Escaper")
    print("Enter your text (press Ctrl+D on Unix/Mac or Ctrl+Z on Windows to finish):")
    print("-" * 50)
    
    try:
        # Read all input
        input_text = sys.stdin.read()
        
        # Escape for JSON
        escaped_text = escape_for_json(input_text)
        
        print("\n" + "=" * 50)
        print("ESCAPED OUTPUT:")
        print("=" * 50)
        print(escaped_text)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)
    except EOFError:
        print("\nNo input provided.")
        sys.exit(1)

if __name__ == "__main__":
    main()