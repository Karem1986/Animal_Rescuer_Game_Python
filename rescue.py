def rescue():
    pet_names = [' kermit', ' Leia', ' bobby', ' tiger', ' kermit', ' Leia', ' bobby', ' tiger']
    age = [ 3, 8, 10, 1, 4, 8, 2, 2]
    hp = [3, 6, 9, 7, 5, 2, 1, 1]

    rescued = []
    for a, name in enumerate(pet_names):
        rescued.append(('name ', name, 'age ', age[a],'healt points: ', hp[a]))
    
    return rescued
    
print(rescue())