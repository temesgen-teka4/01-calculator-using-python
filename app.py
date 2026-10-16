print("==================================")
print("==SMART CALCULATOR USING PYTHON==")
print("===================================")
print(" Type 'q' or 'quit' any time to exit")

while True:
      num1_input=input("Enter the first number : ")
      if num1_input.lower() in ['q','quit']:
            print("Thanks for using Calculator Good Bye!")
            break
      try:
            a=float(num1_input)
            
      except ValueError:
            print("❌ Invalid Input, please enter the valid number")
            continue

      Operator=input("Enter the operation(+,-,/,*): ")
      if Operator.lower()in ['q','quit']:
            print("Thanks for using Calculator Good Bye!")
            break

      num2_input=input("Enter the second number : ")
      if num2_input.lower()in ['q','quit']:
            print("Thanks for using Calculator Good Bye!")
            break
      try:
            b= float(num2_input)
      except ValueError:
            print("❌ Invalid Input,please enter the valid number")
            continue
      match Operator:
            case "+":
                  result=a+b
                  print(f"⭐ ,Result:{a}+{b} ={result}\n")
            case "-":
                  result=a-b
                  print(f"⭐,Result:{a}+{b}={result}\n")
            case "*":
                  result=a*b
                  print(f"⭐,Result:{a}*{b}={result}\n")
            case "/":
                  if b==0:
                        print("Dividing by zero is not allowed")
                  else:
                        result=a/b
                        print(f"⭐,Result:{a}/{b}={result}\n")
            case "_":
                  print(" Invalid Operator!,please use  +,-,/,*\n")

            
    
     
            
 
