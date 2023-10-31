
lst = ["가", "나", "다"]

for lst_idx, lst_val in enumerate(lst):
    print(lst_idx, lst_val)

balls = [1,2,3,4]
weapons = [11,22,3,44]

for ball_idx, ball_val in enumerate(balls):
    print("ball : ", ball_val)
    for weapon_id, weapon_val in enumerate(weapons):
        print("weapons: ", weapon_val)
        if ball_val == weapon_val:
            print("공과 무기가 충돌")
            break
    else:  
        continue
    break        

    # for - else 
    # for에 조건이 안맞으면 else로 
    # else를 통해서 바깥쪽 for 문을 가서 -> 바로 break   

    # if 조건:
    #     동작
    # else: 
    #     그 외의 동작           