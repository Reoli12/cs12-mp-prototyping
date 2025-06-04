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

Model1 = Model(Player1, Settings3, 4, TestEggInfo6, TestEggInfo9, 4)
Model2 = Model(Player2, Settings1, 3, TestEggInfo8, TestEggInfo10, 5)
Model3 = Model(Player3, Settings2, 3, TestEggInfo7, TestEggInfo9, 2)
Model4 = Model(Player4, Settings1, 8, TestEggInfo6, TestEggInfo10, 2)
Model5 = Model(Player5, Settings3, 2, TestEggInfo7, TestEggInfo9, 6)

def test_is_out_of_bounds():
	Player1 = PlayerEgg(TestEggInfo1, TestPoint2, Dmg1, AtkRad1)
	Enemy1 = Eggnemy(TestEggInfo6, TestPoint3)
	Boss1 = Eggnemy(TestEggInfo10, TestPoint6)
	
	out_of_bounds1 = Model1.is_out_of_bounds(Player1)
	out_of_bounds2 = Model2.is_out_of_bounds(Enemy1)
	out_of_bounds3 = Model3.is_out_of_bounds(Boss1)

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

	out_of_bounds4 = Model1.is_out_of_bounds(Player2)
	out_of_bounds5 = Model2.is_out_of_bounds(Enemy2)
	out_of_bounds6 = Model3.is_out_of_bounds(Boss2)
	
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

	out_of_bounds1 = Model1.is_out_of_bounds(Player1)
	out_of_bounds2 = Model2.is_out_of_bounds(Enemy1)
	out_of_bounds3 = Model3.is_out_of_bounds(Boss1)

	assert out_of_bounds1 == True
	assert out_of_bounds2 == True
	assert out_of_bounds3 == True

	return_to_bounds1 = Model1.return_to_bounds(Player1)
	return_to_bounds2 = Model2.return_to_bounds(Enemy1)
	return_to_bounds3 = Model3.return_to_bounds(Boss1)

	out_of_bounds4 = Model1.is_out_of_bounds(Player1)
	out_of_bounds5 = Model2.is_out_of_bounds(Enemy1)
	out_of_bounds6 = Model3.is_out_of_bounds(Boss1)

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

	is_overlapping_player1 = Model1.is_overlapping_player(Enemy1)
	is_overlapping_player2 = Model2.is_overlapping_player(Boss2)
	is_overlapping_player3 = Model3.is_overlapping_player(Enemy3)
	is_overlapping_player4 = Model4.is_overlapping_player(Boss1)
	is_overlapping_player5 = Model5.is_overlapping_player(Enemy2)

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

	is_overlapping_player6 = Model1.is_overlapping_player(Enemy1)
	is_overlapping_player7 = Model2.is_overlapping_player(Boss2)
	is_overlapping_player8 = Model3.is_overlapping_player(Enemy3)
	is_overlapping_player9 = Model4.is_overlapping_player(Boss1)
	is_overlapping_player10 = Model5.is_overlapping_player(Enemy2)

	assert is_overlapping_player6 == False
	assert is_overlapping_player7 == False
	assert is_overlapping_player8 == False
	assert is_overlapping_player9 == False
	assert is_overlapping_player10 == True

	with pytest.raises(TypeError):
		is_overlappingplayer11 = Model1.is_overlapping_player(Player1)

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

	Model1 = Model(Player1, Settings3, 4, TestEggInfo6, TestEggInfo9, 4) #Spd = 11
	Model2 = Model(Player2, Settings1, 3, TestEggInfo8, TestEggInfo10, 5) #Spd = 8
	Model3 = Model(Player3, Settings2, 3, TestEggInfo7, TestEggInfo9, 2) #Spd = 9
	Model4 = Model(Player4, Settings1, 8, TestEggInfo6, TestEggInfo10, 2) #Spd = 7
	Model5 = Model(Player5, Settings3, 2, TestEggInfo7, TestEggInfo9, 6) #Spd = 7

	Model1.player_movement(True, False, False, True)
	Model2.player_movement(True, False, True, True)
	Model3.player_movement(False, True, True, True)
	Model4.player_movement(True, True, False, False)
	Model5.player_movement(True, False, False, True)
	
	
	assert Model1.player_egg.center_position.x == 18.21
	assert Model1.player_egg.center_position.y == -2
	assert Model2.player_egg.center_position.x == 22.1
	assert Model2.player_egg.center_position.y == 4.43
	assert Model3.player_egg.center_position.x == 43.34
	assert Model3.player_egg.center_position.y == 230.56
	assert Model4.player_egg.center_position.x == 2.34
	assert Model4.player_egg.center_position.y == 67.41
	assert Model5.player_egg.center_position.x == 10.5
	assert Model5.player_egg.center_position.y == -2.8

	Model1.player_movement(True, True, True, False)
	Model2.player_movement(False, True, True, False)
	Model3.player_movement(True, True, True, False)
	Model4.player_movement(False, True, True, True)
	Model5.player_movement(True, False, True, True)
	
	assert Model1.player_egg.center_position.x > 7.21
	assert Model1.player_egg.center_position.y == -2
	assert Model2.player_egg.center_position.x > 14.1
	assert Model2.player_egg.center_position.y  == 12.43
	assert Model3.player_egg.center_position.x == 34.34
	assert Model3.player_egg.center_position.y == 230.56
	assert Model4.player_egg.center_position.x == 2.34
	assert Model4.player_egg.center_position.y  == 74.41
	assert Model5.player_egg.center_position.x == 10.5
	assert Model5.player_egg.center_position.y == -9.8

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

	Model1 = Model(Player1, Settings3, 4, TestEggInfo6, TestEggInfo9, 4)
	Model2 = Model(Player2, Settings1, 3, TestEggInfo8, TestEggInfo10, 5)
	Model3 = Model(Player3, Settings2, 3, TestEggInfo7, TestEggInfo9, 2)
	Model4 = Model(Player4, Settings1, 8, TestEggInfo6, TestEggInfo10, 2)
	Model5 = Model(Player5, Settings3, 2, TestEggInfo7, TestEggInfo9, 6)

	Model1.eggnemies.append(Enemy1)
	Model2.eggnemies.append(Enemy3)
	Model3.eggnemies.append(Boss2)
	Model4.eggnemies.append(Boss1)
	Model5.eggnemies.append(Enemy2)

	Model1.player_attack(True)
	assert Enemy1.stats.current_hp == 14
	Model1.player_attack(False)

	Enemy1.center_position.x += 4.63
	Enemy1.center_position.y -= 6.74
	Model1.player_egg.center_position.x -= 24.73
	Model1.player_egg.center_position.y -= 8.4
	Model1.player_attack(True)
	#distance_to_player: float = ((Model1.player_egg.center_position.x - Enemy1.center_position.x) ** 2 + (Model1.player_egg.center_position.y - Enemy1.center_position.y) ** 2) ** 0.5
	#print(distance_to_player)

	assert Enemy1.stats.current_hp == 10
	Model1.player_attack(False)
	
	Model2.player_attack(True)
	assert Enemy3.stats.current_hp == 17
	
	Enemy3.center_position.x -= 3.78
	Enemy3.center_position.y -= 63.56
	Model2.player_egg.center_position.x -= 2.4
	Model2.player_egg.center_position.y += 1.7
	#distance_to_player: float = ((Model2.player_egg.center_position.x - Enemy3.center_position.x) ** 2 + (Model2.player_egg.center_position.y - Enemy3.center_position.y) ** 2) ** 0.5
	#print(distance_to_player)
	Model2.player_attack(True)
	assert Enemy3.stats.current_hp == 12
	
	Boss2.center_position.x -= 10.41
	Boss2.center_position.y -= 59.56
	Model3.player_egg.center_position.x += 14.54
	Model3.player_egg.center_position.y += 160.7
	
	#distance_to_player: float = ((Model3.player_egg.center_position.x - Boss2.center_position.x) ** 2 + (Model3.player_egg.center_position.y - Boss2.center_position.y) ** 2) ** 0.5
	#print(distance_to_player)
	Model3.player_attack(True)
	assert Boss2.stats.current_hp == 29

	Boss2.center_position.x += 0.41
	Boss2.center_position.y -= 1.37
	Player3.center_position.x -= 0.46
	Player3.center_position.y += 0.42
	
	Model3.player_attack(True)
	assert Boss2.stats.current_hp == 23
	
	Model4.player_attack(True)
	assert Boss1.stats.current_hp == 25
	
	Boss1.center_position.x -= 4.45
	Boss1.center_position.y += 6.04
	Player4.center_position.x += 3.46
	Player4.center_position.y -= 4.71
	
	Model4.player_attack(True)
	#distance_to_player: float = ((Model4.player_egg.center_position.x - Boss1.center_position.x) ** 2 + (Model4.player_egg.center_position.y - Boss1.center_position.y) ** 2) ** 0.5
	#print(distance_to_player)
	assert Boss1.stats.current_hp == 25

	Boss1.center_position.x -= 0.451
	Boss1.center_position.y += 1.372
	Model4.player_egg.center_position.x += 3.46
	Model4.player_egg.center_position.y -= 5.71

	Model4.player_attack(True)
	#distance_to_player: float = ((Model4.player_egg.center_position.x - Boss1.center_position.x) ** 2 + (Model4.player_egg.center_position.y - Boss1.center_position.y) ** 2) ** 0.5
	#print(distance_to_player)
	assert Boss1.stats.current_hp == 22

	Model5.player_attack(True)
	assert Enemy2.stats.current_hp == 9
	
	Enemy2.center_position.x -= 3.59
	Enemy2.center_position.y += 5.37
	Model5.player_egg.center_position.x -= 6.46
	Model5.player_egg.center_position.y -= 3.71
	Model5.player_attack(True)
	#distance_to_player: float = ((Model5.player_egg.center_position.x - Enemy2.center_position.x) ** 2 + (Model5.player_egg.center_position.y - Enemy2.center_position.y) ** 2) ** 0.5
	#print(distance_to_player)
	assert Enemy2.stats.current_hp == 9

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


	with pytest.raises(TypeError):
		Model1 = Model(Enemy1, Settings3, 4, EggInfo2, EggInfo4, 4)
		Model2 = Model(Enemy2, Settings1, 3, EggInfo3, EggInfo5, 5)
		Model3 = Model(Enemy3, Settings2, 3, EggInfo4, EggInfo5, 2)
		Model4 = Model(Boss1, Settings1, 8, EggInfo1, EggInfo2, 2)
		Model5 = Model(Boss2, Settings3, 2, EggInfo5, EggInfo1, 6)

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

	is_overlapping_player1 = Model1.is_overlapping_player(Enemy1)
	is_overlapping_player2 = Model2.is_overlapping_player(Boss2)
	is_overlapping_player3 = Model3.is_overlapping_player(Enemy3)
	is_overlapping_player4 = Model4.is_overlapping_player(Boss1)
	is_overlapping_player5 = Model5.is_overlapping_player(Enemy2)

	assert is_overlapping_player1 == False
	assert is_overlapping_player2 == False
	assert is_overlapping_player3 == False
	assert is_overlapping_player4 == True
	assert is_overlapping_player5 == True

	eggnemy_overlap_check1 = Model1.eggnemy_overlap_check(Enemy1)
	eggnemy_overlap_check2 = Model2.eggnemy_overlap_check(Boss2)
	eggnemy_overlap_check3 = Model3.eggnemy_overlap_check(Enemy3)
	eggnemy_overlap_check4 = Model4.eggnemy_overlap_check(Boss1)
	eggnemy_overlap_check5 = Model5.eggnemy_overlap_check(Enemy2)

	assert len(Model1.overlapping_player_eggnemy) == 0
	assert len(Model2.overlapping_player_eggnemy) == 0
	#Note: The following assertion below passes. If pyright somehow flags it just like it does for me, ignore it.
	assert len(Model3.overlapping_player_eggnemy) == 0
	assert len(Model4.overlapping_player_eggnemy) == 1
	assert len(Model5.overlapping_player_eggnemy) == 1

	is_overlapping_player6 = Model1.is_overlapping_player(Boss2)
	is_overlapping_player7 = Model2.is_overlapping_player(Enemy3)
	is_overlapping_player8 = Model3.is_overlapping_player(Enemy2)
	is_overlapping_player9 = Model4.is_overlapping_player(Enemy1)
	is_overlapping_player10 = Model5.is_overlapping_player(Boss1)

	assert is_overlapping_player6 == False
	assert is_overlapping_player7 == False
	assert is_overlapping_player8 == True
	assert is_overlapping_player9 == True
	assert is_overlapping_player10 == True

	eggnemy_overlap_check6 = Model1.eggnemy_overlap_check(Boss2)
	eggnemy_overlap_check7 = Model2.eggnemy_overlap_check(Enemy3)
	eggnemy_overlap_check8 = Model3.eggnemy_overlap_check(Enemy2)
	eggnemy_overlap_check9 = Model4.eggnemy_overlap_check(Enemy1)
	eggnemy_overlap_check10 = Model5.eggnemy_overlap_check(Boss1)

	assert len(Model1.overlapping_player_eggnemy) == 0
	assert len(Model2.overlapping_player_eggnemy) == 0
	assert len(Model3.overlapping_player_eggnemy) == 1
	assert len(Model4.overlapping_player_eggnemy) == 2
	assert len(Model5.overlapping_player_eggnemy) == 2


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
	
	is_overlapping_player11 = Model1.is_overlapping_player(Enemy1)
	is_overlapping_player12 = Model2.is_overlapping_player(Boss2)
	is_overlapping_player13 = Model3.is_overlapping_player(Enemy3)
	is_overlapping_player14 = Model4.is_overlapping_player(Boss1)
	is_overlapping_player15 = Model5.is_overlapping_player(Enemy2)

	assert is_overlapping_player11 == False
	assert is_overlapping_player12 == False
	assert is_overlapping_player13 == False
	assert is_overlapping_player14 == False
	assert is_overlapping_player15 == True

	eggnemy_overlap_check11 = Model1.eggnemy_overlap_check(Enemy1)
	eggnemy_overlap_check12 = Model2.eggnemy_overlap_check(Boss2)
	eggnemy_overlap_check13 = Model3.eggnemy_overlap_check(Enemy3)
	eggnemy_overlap_check14 = Model4.eggnemy_overlap_check(Boss1)
	eggnemy_overlap_check15 = Model5.eggnemy_overlap_check(Enemy2)

	assert len(Model1.overlapping_player_eggnemy) == 0
	assert len(Model2.overlapping_player_eggnemy) == 0
	assert len(Model3.overlapping_player_eggnemy) == 1
	assert len(Model4.overlapping_player_eggnemy) == 1 #Since Boss1 does not overlap anymore, it is removed from the list of overlapping eggnemies.
	assert len(Model5.overlapping_player_eggnemy) == 2 #List of overlapping eggnemies remains unchanged since Enemy2 still overlaps.

	is_overlapping_player16 = Model1.is_overlapping_player(Boss2)
	is_overlapping_player17 = Model2.is_overlapping_player(Enemy3)
	is_overlapping_player18 = Model3.is_overlapping_player(Enemy2)
	is_overlapping_player19 = Model4.is_overlapping_player(Enemy1)
	is_overlapping_player20 = Model5.is_overlapping_player(Boss1)

	assert is_overlapping_player16 == False
	assert is_overlapping_player17 == False
	assert is_overlapping_player18 == False
	assert is_overlapping_player19 == True
	assert is_overlapping_player20 == False

	eggnemy_overlap_check16 = Model1.eggnemy_overlap_check(Boss2)
	eggnemy_overlap_check17 = Model2.eggnemy_overlap_check(Enemy3)
	eggnemy_overlap_check18 = Model3.eggnemy_overlap_check(Enemy2)
	eggnemy_overlap_check19 = Model4.eggnemy_overlap_check(Enemy1)
	eggnemy_overlap_check20 = Model5.eggnemy_overlap_check(Boss1)

	assert len(Model1.overlapping_player_eggnemy) == 0
	assert len(Model2.overlapping_player_eggnemy) == 0
	assert len(Model3.overlapping_player_eggnemy) == 0
	assert len(Model4.overlapping_player_eggnemy) == 1
	assert len(Model5.overlapping_player_eggnemy) == 1 #Since Boss1 does not overlap anymore, it is removed from list of overlapping eggnemies.

def test_restart():
	Model1.player_egg.stats.current_hp -= 451
	Model1.player_egg.stats.height += 482
	Model1.player_egg.stats.width += 127
	Model1.player_egg.stats.max_hp -= 329
	Model1.player_egg.stats.speed -= 32
	Model1.player_egg.center_position.x += 1231
	Model1.player_egg.center_position.y -= 100
	Model1.eggnemies.append(Boss1)
	Model1.overlapping_player_eggnemy.append(Enemy2)

	Model1.restart()

	assert len(Model1.eggnemies) == 0
	assert len(Model1.overlapping_player_eggnemy) == 0
	assert Model1.player_egg.stats.width == 20
	assert Model1.player_egg.stats.height == 40
	assert Model1.player_egg.stats.max_hp == 30
	assert Model1.player_egg.stats.current_hp == 30
	assert Model1.player_egg.stats.speed == 11

def test_game_finished():
	Point1 = deepcopy(TestPoint1)
	Point2 = deepcopy(TestPoint2)
	Point3 = deepcopy(TestPoint3)
	Point4 = deepcopy(TestPoint4)
	Point5 = deepcopy(TestPoint5)

	Point6 = Point(11.34, 2.12)
	Point7 = Point(7.64, 3.9)

	EggInfo1 = deepcopy(TestEggInfo1)
	EggInfo2 = deepcopy(TestEggInfo2)
	EggInfo3 = deepcopy(TestEggInfo3)

	EggInfo4 = deepcopy(TestEggInfo6)
	EggInfo5 = deepcopy(TestEggInfo7)
	EggInfo6 = deepcopy(TestEggInfo8)

	EggInfo7 = EggInfo(50, 50, 6, 6, 6)

	EggInfo8 = EggInfo(40, 40, 6, 6, 3)

	Player1 = PlayerEgg(EggInfo1, Point5, Dmg1, AtkRad1)
	Player2 = PlayerEgg(EggInfo2, Point2, Dmg2, AtkRad2)
	Player3 = PlayerEgg(EggInfo3, Point4, Dmg3, AtkRad3)

	Enemy1 = Eggnemy(EggInfo4, Point3)
	Enemy2 = Eggnemy(EggInfo5, Point1)
	Enemy3 = Eggnemy(EggInfo6, Point4)

	Enemy4 = Eggnemy(EggInfo8, Point6)
	Enemy5 = Eggnemy(EggInfo8, Point7)

	Settings1 = GameSettings(3, 200, 300, 100, 150)

	Model1 = Model(Player1, Settings3, 4, TestEggInfo6, TestEggInfo9, 4)
	Model2 = Model(Player2, Settings1, 3, TestEggInfo8, TestEggInfo9, 5)
	Model3 = Model(Player3, Settings2, 3, EggInfo5, EggInfo7, 1)

	#Scenario 1: Game over due to no more hp.
	Model1.player_egg.stats.current_hp -= Model1.player_egg.stats.current_hp
	assert Model1.player_egg.stats.current_hp == 0
	Model1.update(True, True, False, False, True)
	assert Model1.is_game_over == True

	#Scenario 2: Tracking states before game over.
	Model2.player_egg.stats.current_hp -= 47
	Model2.overlapping_player_eggnemy.append(Enemy1)
	Model2.update(False, True, True, False, True)
	assert Model2.frame_count == 1
	assert Model2.player_egg.stats.current_hp == 2

	Model2.overlapping_player_eggnemy.append(Enemy2)
	Model2.update(False, True, False, True, False)
	assert Model2.frame_count == 2
	assert Model2.player_egg.stats.current_hp == 2
	Model2.update(False, True, False, True, False)

	assert Model2.frame_count == 3
	Model2.overlapping_player_eggnemy.append(Enemy3)

	Model2.update(True, False, False, False, True)
	assert Model2.frame_count == 4
	assert Model2.player_egg.stats.current_hp == 1
	Model2.overlapping_player_eggnemy.remove(Enemy3)
	Model2.update(True, False, False, False, True)
	assert Model2.frame_count == 5
	Model2.overlapping_player_eggnemy.remove(Enemy1)
	Model2.update(True, False, False, False, True)
	assert Model2.frame_count == 6
	assert Model2.player_egg.stats.current_hp == 1 #The model only updates the hp after n + 1 frames wherein n % 2 == 0.
	Model2.update(True, False, False, False, True)
	assert Model2.player_egg.stats.current_hp == 0
	#The call below was necessary since the game_over is called before updating the hp, so the game_over was not called again after the hp turned 0
	Model2.update(True, False, False, False, True)
	assert Model2.frame_count == 7
	assert Model2.is_game_over == True
	
	#Scenario 3: Game done due to defeated boss.
	Model3.eggnemies.append(Enemy4)
	Model3.eggnemies.append(Enemy5)
	print(Model3.player_egg.center_position.x)
	print(Model3.player_egg.center_position.y)
	assert len(Model3.eggnemies) == 2
	Model3.player_attack(True)
	Model3.player_attack(True)
	Model3.update(True, False, False, True, False)
	#print(Model3.boss_egg)
	#Note: The code below may be flagged by pyright, but it does work since there is a boss_egg already. To verify, uncomment the code on the line above.
	Model3.boss_egg.center_position.x = Model3.player_egg.center_position.x - 1
	Model3.boss_egg.center_position.y = Model3.player_egg.center_position.y + 3
	#print(Model3.boss_egg.center_position.x)
	#print(Model3.boss_egg.center_position.y)
	Model3.player_attack(True)
	Model3.update(False, True, True, False, False)
	assert Model3.is_game_won == True
	
def test_leaderboards():
	...