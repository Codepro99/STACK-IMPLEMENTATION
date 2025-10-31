class Stack:
    """Stack class to handle stack operations"""
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Push an item onto the stack"""
        self.items.append(item)
    
    def pop(self):
        """Pop an item from the stack"""
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        """Peek at the top item without removing it"""
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        """Check if stack is empty"""
        return len(self.items) == 0
    
    def size(self):
        """Return the size of the stack"""
        return len(self.items)


def precedence(operator):
    """Return precedence of operators"""
    if operator in ['+', '-']:
        return 1
    elif operator in ['*', '/']:
        return 2
    return 0


def apply_operator(operators, values):
    """Apply operator to values"""
    operator = operators.pop()
    right = values.pop()
    left = values.pop()
    
    if operator == '+':
        values.push(left + right)
    elif operator == '-':
        values.push(left - right)
    elif operator == '*':
        values.push(left * right)
    elif operator == '/':
        if right == 0:
            raise ValueError("Division by zero")
        values.push(left / right)


def evaluate_expression(expression):
    """Evaluate mathematical expression using stack"""
    # Remove whitespace and handle negative numbers
    expression = expression.replace(' ', '')
    
    values = Stack()
    operators = Stack()
    i = 0
    
    while i < len(expression):
        # If current character is a digit, parse the number
        if expression[i].isdigit():
            j = i
            while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                j += 1
            values.push(float(expression[i:j]))
            i = j
        # If current character is '(', push to operators stack
        elif expression[i] == '(':
            operators.push(expression[i])
            i += 1
        # If current character is ')', apply operators until '('
        elif expression[i] == ')':
            while not operators.is_empty() and operators.peek() != '(':
                apply_operator(operators, values)
            operators.pop()  # Remove '('
            i += 1
        # If current character is an operator
        else:
            # Handle negative numbers
            if expression[i] == '-' and (i == 0 or expression[i-1] in ['(', '+', '-', '*', '/']):
                # This is a negative number, not an operator
                j = i + 1
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                values.push(float(expression[i:j]))
                i = j
            else:
                # Regular operator
                while (not operators.is_empty() and 
                       precedence(operators.peek()) >= precedence(expression[i])):
                    apply_operator(operators, values)
                operators.push(expression[i])
                i += 1
    
    # Apply remaining operators
    while not operators.is_empty():
        apply_operator(operators, values)
    
    return values.pop()


def process_file(input_file='input.txt', output_file='output.txt'):
    """Read expressions from input file, evaluate them, and write results to output file"""
    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()
        
        results = []
        
        for line in lines:
            line = line.strip()
            # Check if line is a separator
            if all(c in ['-', ' ', '\t'] for c in line) and len(line) > 0:
                results.append(line)  # Keep the separator as is
            elif line:  # Non-empty line that's not a separator
                try:
                    result = evaluate_expression(line)
                    # Convert to int if it's a whole number, otherwise keep as float
                    if result.is_integer():
                        results.append(str(int(result)))
                    else:
                        results.append(str(result))
                except Exception as e:
                    results.append(f"Error: {str(e)}")
        
        # Write results to output file
        with open(output_file, 'w') as outfile:
            for result in results:
                outfile.write(result + '\n')
        
        print(f"Successfully processed {input_file} and wrote results to {output_file}")
        
    except FileNotFoundError:
        print(f"Error: {input_file} not found")
    except Exception as e:
        print(f"Error processing file: {str(e)}")


def create_sample_input():
    """Create a sample input file for testing"""
    sample_content = """3 + 5 * 2
---
(8 / 4) + 7 * 2
---
10 - (2 + 3) * 4
2 * (3 + 4) - 10 / 2
---
15 + 3 * 2 - 8 / 4"""
    
    with open('input.txt', 'w') as f:
        f.write(sample_content)
    print("Sample input.txt created")


# Main execution
if __name__ == "__main__":
    # Create sample input file
    create_sample_input()
    
    # Process the file
    process_file()
    
    # Display results
    print("\nInput file content:")
    with open('input.txt', 'r') as f:
        print(f.read())
    
    print("Output file content:")
    with open('output.txt', 'r') as f:
        print(f.read())