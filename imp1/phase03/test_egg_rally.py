import pytest
from model import Model
from project_types import Point, PlayerEgg, EggInfo, GameSettings, Eggnemy, Boss
from copy import deepcopy

Dmg1 = 4
Dmg2 = 5
Dmg3 = 6
Dmg4 = 3
Dmg5 = 2

AtkRad1 = 2
AtkRad2 = 6
AtkRad3 = 5
AtkRad4 = 3
AtkRad5 = 4


Settings1 = GameSettings(30, 200, 300, 100, 150)
Settings2 = GameSettings(50, 400, 500, 150, 200)
Settings3 = GameSettings(50, 350, 450, 120, 180)

TestEggInfo1 = EggInfo(20, 40, 30, 30, 11)
TestEggInfo2 = EggInfo(30, 30, 70, 50, 8)
TestEggInfo3 = EggInfo(40, 40, 60, 45, 9)
TestEggInfo4 = EggInfo(50, 50, 20, 10, 7)
TestEggInfo5 = EggInfo(70, 40, 50, 30, 7)

TestEggInfo6 = EggInfo(20, 20, 20, 14, 3)
TestEggInfo7 = EggInfo(30, 30, 15, 9, 2)
TestEggInfo8 = EggInfo(25, 25, 17, 17, 4)

TestEggInfo9 = EggInfo(50, 50, 30, 25, 6)
TestEggInfo10 = EggInfo(50, 50, 35, 35, 7)


TestPoint1 = Point(2, 14)
TestPoint2 = Point(3.5, 4.2)
TestPoint3 = Point(7.21, 9)
TestPoint4 = Point(10.52, 3.6)
TestPoint5 = Point(36.53, 11.75)
TestPoint6 = Point(43, 221.56)
TestPoint7 = Point(22, 12.43)
TestPoint8 = Point(14.24, 12.346)
TestPoint9 = Point(20.87, 0)
TestPoint10 = Point(2.34, 67.41)

Player1 = PlayerEgg(TestEggInfo1, TestPoint5, Dmg1, AtkRad1)
Player2 = PlayerEgg(TestEggInfo2, TestPoint2, Dmg2, AtkRad2)
Player3 = PlayerEgg(TestEggInfo3, TestPoint9, Dmg3, AtkRad3)
Player4 = PlayerEgg(TestEggInfo4, TestPoint1, Dmg4, AtkRad4)
Player5 = PlayerEgg(TestEggInfo5, TestPoint8, Dmg5, AtkRad5)

Enemy1 = Eggnemy(TestEggInfo6, TestPoint3)
Enemy2 = Eggnemy(TestEggInfo7, TestPoint7)
Enemy3 = Eggnemy(TestEggInfo8, TestPoint10)

Boss1 = Boss(TestEggInfo9, TestPoint4)
Boss2 = Boss(TestEggInfo10, TestPoint6)

model1 = Model(Player1, Settings3, 4, TestEggInfo6, TestEggInfo9, 4)
model2 = Model(Player2, Settings1, 3, TestEggInfo8, TestEggInfo10, 5)
model3 = Model(Player3, Settings2, 3, TestEggInfo7, TestEggInfo9, 2)
model4 = Model(Player4, Settings1, 8, TestEggInfo6, TestEggInfo10, 2)
model5 = Model(Player5, Settings3, 2, TestEggInfo7, TestEggInfo9, 6)

def test_is_out_of_bounds():

	Player1 = PlayerEgg(TestEggInfo1, TestPoint2, Dmg1, AtkRad1)
	Enemy1 = Eggnemy(TestEggInfo6, TestPoint3)
	Boss1 = Eggnemy(TestEggInfo10, TestPoint6)
	
	out_of_bounds1 = model1.is_out_of_bounds(Player1)
	out_of_bounds2 = model2.is_out_of_bounds(Enemy1)
	out_of_bounds3 = model3.is_out_of_bounds(Boss1)

	assert out_of_bounds1 == True
	assert out_of_bounds2 == True
	assert out_of_bounds3 == False
	
	EggInfo1 = EggInfo(40, 60, 30, 30, 11)
	EggInfo2 = EggInfo(20, 50, 20, 14, 3)
	EggInfo3 = EggInfo(10, 90, 35, 35, 7)
	Point1 = Point(33.5, 54.2)
	Point2 = Point(27, -3)
	Point3 = Point(83, 266.56)

	Player2 = PlayerEgg(EggInfo1, Point1, Dmg1, AtkRad1)
	Enemy2 = Eggnemy(EggInfo2, Point2)
	Boss2 = Eggnemy(EggInfo3, Point3)

	out_of_bounds4 = model1.is_out_of_bounds(Player2)
	out_of_bounds5 = model2.is_out_of_bounds(Enemy2)
	out_of_bounds6 = model3.is_out_of_bounds(Boss2)
	
	assert out_of_bounds4 == False
	assert out_of_bounds5 == True
	assert out_of_bounds6 == False

def test_return_to_bounds():
	Point1 = Point(13.83, 24.5)
	Point2 = Point(7.32, 9.41)
	Point3 = Point(43, 2.56)

	
	Player1 = PlayerEgg(TestEggInfo5, Point1, Dmg1, AtkRad1)
	Enemy1 = Eggnemy(TestEggInfo6, Point2)
	Boss1 = Eggnemy(TestEggInfo7, Point3)

	out_of_bounds1 = model1.is_out_of_bounds(Player1)
	out_of_bounds2 = model2.is_out_of_bounds(Enemy1)
	out_of_bounds3 = model3.is_out_of_bounds(Boss1)

	assert out_of_bounds1 == True
	assert out_of_bounds2 == True
	assert out_of_bounds3 == True

	return_to_bounds1 = model1.return_to_bounds(Player1)
	return_to_bounds2 = model2.return_to_bounds(Enemy1)
	return_to_bounds3 = model3.return_to_bounds(Boss1)

	out_of_bounds4 = model1.is_out_of_bounds(Player1)
	out_of_bounds5 = model2.is_out_of_bounds(Enemy1)
	out_of_bounds6 = model3.is_out_of_bounds(Boss1)

	assert out_of_bounds4 == False
	assert out_of_bounds5 == False
	assert out_of_bounds6 == False

def test_is_overlapping_player():
	
	Point1 = deepcopy(TestPoint1)
	Point2 = deepcopy(TestPoint2)
	Point3 = deepcopy(TestPoint3)
	Point4 = deepcopy(TestPoint4)
	Point5 = deepcopy(TestPoint5)
	Point6 = deepcopy(TestPoint6)
	Point7 = deepcopy(TestPoint7)
	Point8 = deepcopy(TestPoint8)
	Point9 = deepcopy(TestPoint9)
	Point10 = deepcopy(TestPoint10)

	Player1 = PlayerEgg(TestEggInfo1, Point5, Dmg1, AtkRad1)
	Player2 = PlayerEgg(TestEggInfo2, Point2, Dmg2, AtkRad2)
	Player3 = PlayerEgg(TestEggInfo3, Point9, Dmg3, AtkRad3)
	Player4 = PlayerEgg(TestEggInfo4, Point1, Dmg4, AtkRad4)
	Player5 = PlayerEgg(TestEggInfo5, Point8, Dmg5, AtkRad5)

	Enemy1 = Eggnemy(TestEggInfo6, Point3)
	Enemy2 = Eggnemy(TestEggInfo7, Point7)
	Enemy3 = Eggnemy(TestEggInfo8, Point10)

	Boss1 = Boss(TestEggInfo9, Point4)
	Boss2 = Boss(TestEggInfo10, Point6)

	is_overlapping_player1 = model1.is_overlapping_player(Enemy1)
	is_overlapping_player2 = model2.is_overlapping_player(Boss2)
	is_overlapping_player3 = model3.is_overlapping_player(Enemy3)
	is_overlapping_player4 = model4.is_overlapping_player(Boss1)
	is_overlapping_player5 = model5.is_overlapping_player(Enemy2)

	assert is_overlapping_player1 == False
	assert is_overlapping_player2 == False
	assert is_overlapping_player3 == False
	assert is_overlapping_player4 == True
	assert is_overlapping_player5 == True

	Player1.center_position.x += 30
	Enemy1.center_position.y += 23
	Player2.center_position.y += 43.7
	Enemy2.center_position.y += 24.4
	Player3.center_position.x += 24.5
	Enemy3.center_position.y += 32.3
	Player4.center_position.y += 25.6
	Boss1.center_position.y -= 45.3
	Player5.center_position.x += 34.73
	Boss2.center_position.x -= 45.3

	is_overlapping_player6 = model1.is_overlapping_player(Enemy1)
	is_overlapping_player7 = model2.is_overlapping_player(Boss2)
	is_overlapping_player8 = model3.is_overlapping_player(Enemy3)
	is_overlapping_player9 = model4.is_overlapping_player(Boss1)
	is_overlapping_player10 = model5.is_overlapping_player(Enemy2)

	assert is_overlapping_player6 == False
	assert is_overlapping_player7 == False
	assert is_overlapping_player8 == False
	assert is_overlapping_player9 == False
	assert is_overlapping_player10 == True

	with pytest.raises(TypeError):
		is_overlappingplayer11 = model1.is_overlapping_player(Player1)

def test_player_movement():
	
	Point1 = Point(3.5, 4.2)
	Point2 = Point(7.21, 9)
	Point3 = Point(43.34, 221.56)
	Point4 = Point(22.1, 12.43)
	Point5 = Point(2.34, 67.41)

	Player1 = PlayerEgg(TestEggInfo1, Point2, Dmg1, AtkRad1)
	Player2 = PlayerEgg(TestEggInfo2, Point4, Dmg2, AtkRad2)
	Player3 = PlayerEgg(TestEggInfo3, Point3, Dmg3, AtkRad3)
	Player4 = PlayerEgg(TestEggInfo4, Point5, Dmg4, AtkRad4)
	Player5 = PlayerEgg(TestEggInfo5, Point1, Dmg5, AtkRad5)


	model1.player_movement(True, False, False, True)
	model1.player_movement(True, True, True, False)
	model2.player_movement(True, False, True, True)
	model2.player_movement(False, True, True, False)
	model3.player_movement(False, True, True, True)
	model3.player_movement(True, True, True, False)
	model4.player_movement(True, True, False, False)
	model4.player_movement(False, True, True, True)
	model5.player_movement(True, False, False, True)
	model5.player_movement(True, False, True, True)

	assert Player1.center_position.x == 7.21
	assert Player1.center_position.y == 9
	assert Player2.center_position.x == 22.1
	assert Player2.center_position.y == 12.43
	assert Player3.center_position.x == 43.34
	assert Player3.center_position.y == 221.56
	assert Player4.center_position.x == 2.34
	assert Player4.center_position.y == 67.41
	assert Player5.center_position.x == 3.5
	assert Player5.center_position.y == 4.2

def test_player_attack():
	EggInfo1 = deepcopy(TestEggInfo1)
	EggInfo2 = deepcopy(TestEggInfo2)
	EggInfo3 = deepcopy(TestEggInfo3)
	EggInfo4 = deepcopy(TestEggInfo4)
	EggInfo5 = deepcopy(TestEggInfo5)

	EggInfo6 = deepcopy(TestEggInfo6)
	EggInfo7 = deepcopy(TestEggInfo7)
	EggInfo8 = deepcopy(TestEggInfo8)

	EggInfo9 = deepcopy(TestEggInfo9)
	EggInfo10 = deepcopy(TestEggInfo10)


	Point1 = deepcopy(TestPoint1)
	Point2 = deepcopy(TestPoint2)
	Point3 = deepcopy(TestPoint3)
	Point4 = deepcopy(TestPoint4)
	Point5 = deepcopy(TestPoint5)
	Point6 = deepcopy(TestPoint6)
	Point7 = deepcopy(TestPoint7)
	Point8 = deepcopy(TestPoint8)
	Point9 = deepcopy(TestPoint9)
	Point10 = deepcopy(TestPoint10)

	Player1 = PlayerEgg(EggInfo1, Point5, Dmg1, AtkRad1)
	Player2 = PlayerEgg(EggInfo2, Point2, Dmg2, AtkRad2)
	Player3 = PlayerEgg(EggInfo3, Point9, Dmg3, AtkRad3)
	Player4 = PlayerEgg(EggInfo4, Point1, Dmg4, AtkRad4)
	Player5 = PlayerEgg(EggInfo5, Point8, Dmg5, AtkRad5)

	Enemy1 = Eggnemy(EggInfo6, Point3)
	Enemy2 = Eggnemy(EggInfo7, Point7)
	Enemy3 = Eggnemy(EggInfo8, Point10)

	Boss1 = Boss(EggInfo9, Point4)
	Boss2 = Boss(EggInfo10, Point6)

	model1 = Model(Player1, Settings3, 4, TestEggInfo6, TestEggInfo9, 4)
	model2 = Model(Player2, Settings1, 3, TestEggInfo8, TestEggInfo10, 5)
	model3 = Model(Player3, Settings2, 3, TestEggInfo7, TestEggInfo9, 2)
	model4 = Model(Player4, Settings1, 8, TestEggInfo6, TestEggInfo10, 2)
	model5 = Model(Player5, Settings3, 2, TestEggInfo7, TestEggInfo9, 6)

	model1.eggnemies.append(Enemy1)
	model2.eggnemies.append(Enemy3)
	model3.eggnemies.append(Boss2)
	model4.eggnemies.append(Boss1)
	model5.eggnemies.append(Enemy2)

	model1.player_attack(True)
	assert Enemy1.stats.current_hp == 14
	model1.player_attack(False)

	Enemy1.center_position.x += 4.63
	Enemy1.center_position.y -= 6.74
	Player1.center_position.x -= 24.73
	Player1.center_position.y -= 8.4
	model1.player_attack(True)
	#distance_to_player: float = ((Player1.center_position.x - Enemy1.center_position.x) ** 2 + (Player1.center_position.y - Enemy1.center_position.y) ** 2) ** 0.5
	#print(distance_to_player)
	assert Enemy1.stats.current_hp == 10
	model1.player_attack(False)
	
	model2.player_attack(True)
	assert Enemy3.stats.current_hp == 17
	
	Enemy3.center_position.x -= 3.78
	Enemy3.center_position.y -= 63.56
	Player2.center_position.x -= 2.4
	Player2.center_position.y += 1.7
	
	model2.player_attack(True)
	assert Enemy3.stats.current_hp == 12
	
	Boss2.center_position.x -= 10.41
	Boss2.center_position.y -= 59.56
	Player3.center_position.x += 14.54
	Player3.center_position.y += 160.7
	
	#distance_to_player: float = ((Player3.center_position.x - Boss2.center_position.x) ** 2 + (Player3.center_position.y - Boss2.center_position.y) ** 2) ** 0.5
	#print(distance_to_player)
	model3.player_attack(True)
	assert Boss2.stats.current_hp == 29

	Boss2.center_position.x += 0.41
	Boss2.center_position.y -= 1.37
	Player3.center_position.x -= 0.46
	Player3.center_position.y += 0.42
	
	model3.player_attack(True)
	assert Boss2.stats.current_hp == 23
	
	model4.player_attack(True)
	assert Boss1.stats.current_hp == 25
	
	Boss1.center_position.x -= 4.45
	Boss1.center_position.y += 6.04
	Player4.center_position.x += 3.46
	Player4.center_position.y -= 4.71
	
	model4.player_attack(True)
	#distance_to_player: float = ((Player4.center_position.x - Boss1.center_position.x) ** 2 + (Player4.center_position.y - Boss1.center_position.y) ** 2) ** 0.5
	#print(distance_to_player)
	assert Boss1.stats.current_hp == 22

	Boss1.center_position.x -= 4.45
	Boss1.center_position.y += 4.37
	Player4.center_position.x += 3.46
	Player4.center_position.y -= 5.71

	model4.player_attack(True)
	assert Boss1.stats.current_hp == 22

	model5.player_attack(True)
	assert Enemy2.stats.current_hp == 9
	
	Enemy2.center_position.x -= 3.59
	Enemy2.center_position.y += 5.37
	Player5.center_position.x -= 6.46
	Player5.center_position.y -= 3.71
	model5.player_attack(True)
	assert Enemy2.stats.current_hp == 9

	#distance_to_player: float = ((Player5.center_position.x - Enemy2.center_position.x) ** 2 + (Player5.center_position.y - Enemy2.center_position.y) ** 2) ** 0.5
	#print(distance_to_player)

def test_incompatible_model_init():
	EggInfo1 = EggInfo(20, 20, 20, 14, 3)
	EggInfo2 = EggInfo(30, 30, 15, 9, 2)
	EggInfo3 = EggInfo(25, 25, 17, 17, 4)

	EggInfo4 = EggInfo(50, 50, 30, 25, 6)
	EggInfo5 = EggInfo(50, 50, 35, 35, 7)


	Point1 = Point(2, 14)
	Point2 = Point(3.5, 4.2)
	Point3 = Point(7.21, 9)
	Point4 = Point(10.52, 3.6)
	Point5 = Point(36.53, 11.75)

	Enemy1 = Eggnemy(EggInfo1, Point1)
	Enemy2 = Eggnemy(EggInfo2, Point2)
	Enemy3 = Eggnemy(EggInfo3, Point3)

	Boss1 = Boss(EggInfo4, Point4)
	Boss2 = Boss(EggInfo5, Point5)


	with pytest.raises(ValueError):
		model1 = Model(Enemy1, Settings3, 4, EggInfo2, EggInfo4, 4)
		model2 = Model(Enemy2, Settings1, 3, EggInfo3, EggInfo5, 5)
		model3 = Model(Enemy3, Settings2, 3, EggInfo4, EggInfo5, 2)
		model4 = Model(Boss1, Settings1, 8, EggInfo1, EggInfo2, 2)
		model5 = Model(Boss2, Settings3, 2, EggInfo5, EggInfo1, 6)
	
'''
Test:
Restart, eggnemy overlap check, controller and model gameover, controller and model leaderboards
'''
def test_eggnemy_overlap_check():
	Point1 = deepcopy(TestPoint1)
	Point2 = deepcopy(TestPoint2)
	Point3 = deepcopy(TestPoint3)
	Point4 = deepcopy(TestPoint4)
	Point5 = deepcopy(TestPoint5)
	Point6 = deepcopy(TestPoint6)
	Point7 = deepcopy(TestPoint7)
	Point8 = deepcopy(TestPoint8)
	Point9 = deepcopy(TestPoint9)
	Point10 = deepcopy(TestPoint10)

	Player1 = PlayerEgg(TestEggInfo1, Point5, Dmg1, AtkRad1)
	Player2 = PlayerEgg(TestEggInfo2, Point2, Dmg2, AtkRad2)
	Player3 = PlayerEgg(TestEggInfo3, Point9, Dmg3, AtkRad3)
	Player4 = PlayerEgg(TestEggInfo4, Point1, Dmg4, AtkRad4)
	Player5 = PlayerEgg(TestEggInfo5, Point8, Dmg5, AtkRad5)

	Enemy1 = Eggnemy(TestEggInfo6, Point3)
	Enemy2 = Eggnemy(TestEggInfo7, Point7)
	Enemy3 = Eggnemy(TestEggInfo8, Point10)

	Boss1 = Boss(TestEggInfo9, Point4)
	Boss2 = Boss(TestEggInfo10, Point6)

	is_overlapping_player1 = model1.is_overlapping_player(Enemy1)
	is_overlapping_player2 = model2.is_overlapping_player(Boss2)
	is_overlapping_player3 = model3.is_overlapping_player(Enemy3)
	is_overlapping_player4 = model4.is_overlapping_player(Boss1)
	is_overlapping_player5 = model5.is_overlapping_player(Enemy2)

	assert is_overlapping_player1 == False
	assert is_overlapping_player2 == False
	assert is_overlapping_player3 == False
	assert is_overlapping_player4 == True
	assert is_overlapping_player5 == True

	eggnemy_overlap_check1 = model1.eggnemy_overlap_check(Enemy1)
	eggnemy_overlap_check2 = model2.eggnemy_overlap_check(Boss2)
	eggnemy_overlap_check3 = model3.eggnemy_overlap_check(Enemy3)
	eggnemy_overlap_check4 = model4.eggnemy_overlap_check(Boss1)
	eggnemy_overlap_check5 = model5.eggnemy_overlap_check(Enemy2)

	is_overlapping_player6 = model1.is_overlapping_player(Boss2)
	is_overlapping_player7 = model2.is_overlapping_player(Enemy3)
	is_overlapping_player8 = model3.is_overlapping_player(Enemy2)
	is_overlapping_player9 = model4.is_overlapping_player(Enemy1)
	is_overlapping_player10 = model5.is_overlapping_player(Boss1)

	eggnemy_overlap_check1 = model1.eggnemy_overlap_check(Boss2)
	eggnemy_overlap_check2 = model2.eggnemy_overlap_check(Enemy3)
	eggnemy_overlap_check3 = model3.eggnemy_overlap_check(Enemy2)
	eggnemy_overlap_check4 = model4.eggnemy_overlap_check(Enemy1)
	eggnemy_overlap_check5 = model5.eggnemy_overlap_check(Boss1)

	print(is_overlapping_player6)
	print(is_overlapping_player7)
	print(is_overlapping_player8)
	print(is_overlapping_player9)
	print(is_overlapping_player10)

def test_restart ():
	...
test_eggnemy_overlap_check()