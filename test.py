def split_string(input_string):
    # Calculate the number of substrings required
    num_substrings = len(input_string) // 500 + \
        (1 if len(input_string) % 500 > 0 else 0)

    # Split the input string into substrings of 500 characters each
    substrings = [input_string[i * 500:(i + 1) * 500]
                  for i in range(num_substrings)]

    return substrings


# Test the function with a sample string
sample_string = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur pretium lacinia dui, eget suscipit mauris fringilla vel. Donec nec lacus vitae sapien cursus bibendum. Proin accumsan tortor et mi fermentum, in ullamcorper neque tempor. Pellentesque sollicitudin ante a odio bibendum, ac ullamcorper sapien semper.

- Maecenas vel aliquam elit, vitae cursus metus.
- Sed auctor odio sed ligula ultrices, at lacinia mi vestibulum.
- In hac habitasse platea dictumst. Suspendisse facilisis justo quis enim dictum, vel fermentum magna posuere.

Praesent ullamcorper luctus velit, ac bibendum nisi bibendum ut. Integer venenatis ultricies odio, non mollis nisl dignissim id. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Mauris ut lectus id justo feugiat lacinia. Donec euismod, lectus ut feugiat tristique, nisl eros cursus nulla, in ultrices libero sem eu neque.

Etiam pharetra turpis nec metus accumsan, at sollicitudin augue posuere. Cras scelerisque dui nec eros congue, id molestie sapien consequat. Nullam at sapien eu dui aliquet fringilla. Aenean vitae arcu vel lacus tempus facilisis. Fusce tristique, libero non pellentesque luctus, mi odio ullamcorper sapien, a malesuada felis quam vel leo. Morbi at nibh vel justo blandit dapibus.

Sed vestibulum eleifend velit, ac porttitor ante vulputate et. Curabitur at lacus nec augue accumsan viverra. In eget quam nec nunc facilisis pretium. Nunc auctor, odio nec ullamcorper scelerisque, lacus elit fringilla est, in commodo odio lacus vitae lorem. Fusce id ante id sapien dapibus congue. Vivamus auctor elit et nisl fringilla, eget rhoncus nunc semper.
'''
substrings_list = split_string(sample_string)

# Output the substrings to the console
for i, substring in enumerate(substrings_list):
    print("")
    print(f"{substring}")
    print("")
