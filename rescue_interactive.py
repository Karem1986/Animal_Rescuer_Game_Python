user_name = input('Please enter your name')

# check for number
def is_number():
    check_for_number = user_name.isnumeric()
    return check_for_number

# Assign score based on how many pets are rescued
SCORE = 0
def score_user():
   global SCORE
   SCORE +=3
   return SCORE
   
def rescue():
    # Input validation
    if is_number():
        print('Not a name, please enter your name')
     # Third, greet the user and welcome them to the game
    else:
      greet = 'Welcome ' + user_name + ' To the game! You will be in no time a real Hero Animal Rescuer!'
      print(greet)
	
    # Third, show the user the game explanation and then show the pets names to be rescued
      game_explt = 'Choose how many cats or dogs you wanna rescue, you will receive a score from 1 to 10, more pets == higher score. ' 
      print(game_explt)

      print("These are the cats in the shelter: ")
      cat_names = [' Kermit', 'Leia', ' Bobby', ' Tiger', ' Asos', 'Guizmo', 'Suffo', 'Marraket', 'Kiki', 'Ursula']
      print(cat_names)
      cat_age = [ 3, 8, 12, 1, 4, 8, 2, 2, 8, 4]
      print("Their age: ", cat_age)
      cat_hs = [3, 6, 9, 7, 5, 2, 1, 1, 2, 3]
      print("Their health score: ", cat_hs)
      # DOGS
      print("These are the dogs in the shelter: ")
      dog_names = [' Kermit', 'Leia', ' Bobby', ' Tiger', ' Asos', 'Guizmo', 'Suffo', 'Marraket', 'Kiki', 'Ursula']
      print(dog_names)
      dog_age = [ 3, 8, 12, 1, 4, 8, 2, 2, 8, 4]
      print("Their age: ", dog_age)
      dog_hs = [3, 6, 9, 7, 5, 2, 1, 1, 2, 3]
      print("Their health score: ", dog_hs)

    # How many pets can you rescue? 
      howManyrescue = input(str('How many pets can you rescue?'))
      toInt = int(howManyrescue)
  
    # #  Cat or dog
    #   pet = input(str('A cat or a dog?'))
    #   print((pet))
      
    # if user inputs 0, ask to rescue minimum one pet
      if toInt == 0:
          print("Minimum to rescue one pet!")
     # If user can rescue one pet: print the pet's name, the score and a thank you message. 
      elif toInt == 1:
        pet = input(str('A cat or a dog?'))
        print((pet))
        if pet == 'cat':
          print(f"The cat's name is:", cat_names[0], "His health score is: ", cat_hs[0], "Your score is:", score_user())
        elif pet == 'dog':
          print(f"The dog's name is:", dog_names[0], "His health score is: ", dog_hs[0], "Your score is:", score_user())
      elif toInt > 1 and toInt < 3:
          cats = str(input("Do you want to rescue 2 cats or 2 dogs?"))
          print(cats)
          if cats == 'two cats':
              print(f"The cat's names are:", cat_names[:2], "Their health score: ", cat_hs[:2], "Your score is:", score_user())
          
      # rescued = []
      # for a, name in enumerate(cat_names):
      #   rescued.append(('name ', name, 'age ', cat_age[a],'healt points: ', cat_hs[a]))
    
      # return rescued
    
print(rescue())