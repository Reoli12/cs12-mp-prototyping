import pytest
from model import EgghancementSettings, Model
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

TestEggInfo1 = EggInfo(20, 40, 30, 30, 4, 11)
TestEggInfo2 = EggInfo(30, 30, 70, 50, 5, 8)
TestEggInfo3 = EggInfo(40, 40, 60, 45, 6, 9)
TestEggInfo4 = EggInfo(50, 50, 20, 10, 3, 7)
TestEggInfo5 = EggInfo(70, 40, 50, 30, 2, 7)

TestEggInfo6 = EggInfo(20, 20, 20, 14, 1, 3)
TestEggInfo7 = EggInfo(30, 30, 15, 9, 4, 2)
TestEggInfo8 = EggInfo(25, 25, 17, 17, 3, 4)

TestEggInfo9 = EggInfo(50, 50, 30, 25, 8, 6)
TestEggInfo10 = EggInfo(50, 50, 35, 35, 9, 7)


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

EgghancementSettings1 = EgghancementSettings(8, 10, 5, 4)
EgghancementSettings2 = EgghancementSettings(15, 8, 3, 6)
EgghancementSettings3 = EgghancementSettings(11, 6, 7, 2)
EgghancementSettings4 = EgghancementSettings(13, 7, 4, 5)
EgghancementSettings5 = EgghancementSettings(14, 9, 2, 3)

TestPlayer1 = PlayerEgg(TestEggInfo1, TestPoint5, AtkRad1)
TestPlayer2 = PlayerEgg(TestEggInfo2, TestPoint2, AtkRad2)
TestPlayer3 = PlayerEgg(TestEggInfo3, TestPoint9, AtkRad3)
TestPlayer4 = PlayerEgg(TestEggInfo4, TestPoint1, AtkRad4)
TestPlayer5 = PlayerEgg(TestEggInfo5, TestPoint8, AtkRad5)

Enemy1 = Eggnemy(TestEggInfo6, TestPoint3)
Enemy2 = Eggnemy(TestEggInfo7, TestPoint7)
Enemy3 = Eggnemy(TestEggInfo8, TestPoint10)

Boss1 = Boss(TestEggInfo9, TestPoint4)
Boss2 = Boss(TestEggInfo10, TestPoint6)

TestModel1 = Model(TestPlayer1, Settings3, 4, TestEggInfo6, TestEggInfo9, 4, EgghancementSettings1)
TestModel2 = Model(TestPlayer2, Settings1, 3, TestEggInfo8, TestEggInfo10, 5, EgghancementSettings2)
TestModel3 = Model(TestPlayer3, Settings2, 3, TestEggInfo7, TestEggInfo9, 2, EgghancementSettings3)
TestModel4 = Model(TestPlayer4, Settings1, 8, TestEggInfo6, TestEggInfo10, 2, EgghancementSettings4)
TestModel5 = Model(TestPlayer5, Settings3, 2, TestEggInfo7, TestEggInfo9, 6, EgghancementSettings5)

def test_is_out_of_bounds():
	Player1 = PlayerEgg(TestEggInfo1, TestPoint2, AtkRad1)
	Enemy1 = Eggnemy(TestEggInfo6, TestPoint3)
	Boss1 = Eggnemy(TestEggInfo10, TestPoint6)
	
	out_of_bounds1 = TestModel1.is_out_of_world_bounds(Player1)
	out_of_bounds2 = TestModel2.is_out_of_world_bounds(Enemy1)
	out_of_bounds3 = TestModel3.is_out_of_world_bounds(Boss1)

	assert out_of_bounds1 == True
	assert out_of_bounds2 == True
	assert out_of_bounds3 == False
	
	EggInfo1 = deepcopy(TestEggInfo1)
	EggInfo2 = deepcopy(TestEggInfo2)
	EggInfo3 = deepcopy(TestEggInfo3)
	Point1 = Point(33.5, 54.2)
	Point2 = Point(27, -3)
	Point3 = Point(83, 266.56)

	Player2 = PlayerEgg(EggInfo1, Point1, AtkRad1)
	Enemy2 = Eggnemy(EggInfo2, Point2)
	Boss2 = Eggnemy(EggInfo3, Point3)

	out_of_bounds4 = TestModel1.is_out_of_world_bounds(Player2)
	out_of_bounds5 = TestModel2.is_out_of_world_bounds(Enemy2)
	out_of_bounds6 = TestModel3.is_out_of_world_bounds(Boss2)
	
	assert out_of_bounds4 == False
	assert out_of_bounds5 == True
	assert out_of_bounds6 == False

def test_return_to_bounds():
	Point1 = Point(13.83, 24.5)
	Point2 = Point(7.32, 9.41)
	Point3 = Point(43, 2.56)
	
	Player1 = PlayerEgg(TestEggInfo5, Point1, AtkRad1)
	Enemy1 = Eggnemy(TestEggInfo6, Point2)
	Boss1 = Eggnemy(TestEggInfo7, Point3)

	out_of_bounds1 = TestModel1.is_out_of_world_bounds(Player1)
	out_of_bounds2 = TestModel2.is_out_of_world_bounds(Enemy1)
	out_of_bounds3 = TestModel3.is_out_of_world_bounds(Boss1)

	assert out_of_bounds1 == True
	assert out_of_bounds2 == True
	assert out_of_bounds3 == True

	return_to_bounds1 = TestModel1.return_to_world_bounds(Player1)
	return_to_bounds2 = TestModel2.return_to_world_bounds(Enemy1)
	return_to_bounds3 = TestModel3.return_to_world_bounds(Boss1)

	out_of_bounds4 = TestModel1.is_out_of_world_bounds(Player1)
	out_of_bounds5 = TestModel2.is_out_of_world_bounds(Enemy1)
	out_of_bounds6 = TestModel3.is_out_of_world_bounds(Boss1)

	assert out_of_bounds4 == False
	assert out_of_bounds5 == False
	assert out_of_bounds6 == False


def test_player_movement():
	Model1 = deepcopy(TestModel1) #Spd = 11
	Model2 = deepcopy(TestModel2) #Spd = 8
	Model3 = deepcopy(TestModel3) #Spd = 9
	Model4 = deepcopy(TestModel4) #Spd = 7
	Model5 = deepcopy(TestModel5) #Spd = 7

	Model1.player_movement(True, False, False, True)
	Model2.player_movement(True, False, True, True)
	Model3.player_movement(False, True, True, True)
	Model4.player_movement(True, True, False, False)
	Model5.player_movement(True, False, False, True)
	
	
	assert Model1.player_egg.center_position.x == 47.53
	assert Model1.player_egg.center_position.y == 0.75
	assert Model2.player_egg.center_position.x == 3.5
	assert Model2.player_egg.center_position.y == -3.8
	assert Model3.player_egg.center_position.x == 20.87
	assert Model3.player_egg.center_position.y == 9
	assert Model4.player_egg.center_position.x == 2
	assert Model4.player_egg.center_position.y == 14
	assert Model5.player_egg.center_position.x > 21.24
	assert Model5.player_egg.center_position.y == 5.346

	Model1.player_movement(True, True, True, False)
	Model2.player_movement(False, True, True, False)
	Model3.player_movement(True, True, True, False)
	Model4.player_movement(False, True, True, True)
	Model5.player_movement(True, False, True, True)
	
	assert Model1.player_egg.center_position.x == 36.53
	assert Model1.player_egg.center_position.y == 0.75
	assert Model2.player_egg.center_position.x == -4.5
	assert Model2.player_egg.center_position.y  == 4.2
	assert Model3.player_egg.center_position.x > 11.87
	assert Model3.player_egg.center_position.y == 9
	assert Model4.player_egg.center_position.x == 2
	assert Model4.player_egg.center_position.y  == 21
	assert Model5.player_egg.center_position.x > 21.24
	assert Model5.player_egg.center_position.y == -1.654

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

	Player1 = PlayerEgg(EggInfo1, Point5, AtkRad1)
	Player2 = PlayerEgg(EggInfo2, Point2, AtkRad2)
	Player3 = PlayerEgg(EggInfo3, Point9, AtkRad3)
	Player4 = PlayerEgg(EggInfo4, Point1, AtkRad4)
	Player5 = PlayerEgg(EggInfo5, Point8, AtkRad5)

	Enemy1 = Eggnemy(EggInfo6, Point3)
	Enemy2 = Eggnemy(EggInfo7, Point7)
	Enemy3 = Eggnemy(EggInfo8, Point10)

	Boss1 = Boss(EggInfo9, Point4)
	Boss2 = Boss(EggInfo10, Point6)

	Model1 = deepcopy(TestModel1)
	Model2 = deepcopy(TestModel2)
	Model3 = deepcopy(TestModel3)
	Model4 = deepcopy(TestModel4)
	Model5 = deepcopy(TestModel5)

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
	EggInfo1 = deepcopy(TestEggInfo6)
	EggInfo2 = deepcopy(TestEggInfo7)
	EggInfo3 = deepcopy(TestEggInfo8)

	EggInfo4 = deepcopy(TestEggInfo9)
	EggInfo5 = deepcopy(TestEggInfo10)


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
		Model1 = Model(Enemy1, Settings3, 4, EggInfo2, EggInfo4, 4, EgghancementSettings1)
		Model2 = Model(Enemy2, Settings1, 3, EggInfo3, EggInfo5, 5, EgghancementSettings2)
		Model3 = Model(Enemy3, Settings2, 3, EggInfo4, EggInfo5, 2, EgghancementSettings3)
		Model4 = Model(Boss1, Settings1, 8, EggInfo1, EggInfo2, 2, EgghancementSettings4)
		Model5 = Model(Boss2, Settings3, 2, EggInfo5, EggInfo1, 6, EgghancementSettings5)

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

	Player1 = deepcopy(TestPlayer1)
	Player2 = deepcopy(TestPlayer2)
	Player3 = deepcopy(TestPlayer3)
	Player4 = deepcopy(TestPlayer4)
	Player5 = deepcopy(TestPlayer5)

	Enemy1 = Eggnemy(TestEggInfo6, Point3)
	Enemy2 = Eggnemy(TestEggInfo7, Point7)
	Enemy3 = Eggnemy(TestEggInfo8, Point10)

	Boss1 = Boss(TestEggInfo9, Point4)
	Boss2 = Boss(TestEggInfo10, Point6)

	is_overlapping_player1 = TestModel1.is_overlapping_entities(Enemy1, TestModel1.player_egg)
	is_overlapping_player2 = TestModel2.is_overlapping_entities(Boss2, TestModel2.player_egg)
	is_overlapping_player3 = TestModel3.is_overlapping_entities(Enemy3, TestModel3.player_egg)
	is_overlapping_player4 = TestModel4.is_overlapping_entities(Boss1, TestModel4.player_egg)
	is_overlapping_player5 = TestModel5.is_overlapping_entities(Enemy2, TestModel5.player_egg)

	assert is_overlapping_player1 == False
	assert is_overlapping_player2 == False
	assert is_overlapping_player3 == False
	assert is_overlapping_player4 == True
	assert is_overlapping_player5 == True

	eggnemy_overlap_check1 = TestModel1.eggnemy_overlap_check(Enemy1)
	eggnemy_overlap_check2 = TestModel2.eggnemy_overlap_check(Boss2)
	eggnemy_overlap_check3 = TestModel3.eggnemy_overlap_check(Enemy3)
	eggnemy_overlap_check4 = TestModel4.eggnemy_overlap_check(Boss1)
	eggnemy_overlap_check5 = TestModel5.eggnemy_overlap_check(Enemy2)

	assert len(TestModel1.overlapping_player_eggnemy) == 0
	assert len(TestModel2.overlapping_player_eggnemy) == 0
	assert len(TestModel3.overlapping_player_eggnemy) == 0
	assert len(TestModel4.overlapping_player_eggnemy) == 1
	assert len(TestModel5.overlapping_player_eggnemy) == 1

	is_overlapping_player6 = TestModel1.is_overlapping_entities(Boss2, TestModel1.player_egg)
	is_overlapping_player7 = TestModel2.is_overlapping_entities(Enemy3, TestModel2.player_egg)
	is_overlapping_player8 = TestModel3.is_overlapping_entities(Enemy2, TestModel3.player_egg)
	is_overlapping_player9 = TestModel4.is_overlapping_entities(Enemy1, TestModel4.player_egg)
	is_overlapping_player10 = TestModel5.is_overlapping_entities(Boss1, TestModel5.player_egg)

	assert is_overlapping_player6 == False
	assert is_overlapping_player7 == False
	assert is_overlapping_player8 == True
	assert is_overlapping_player9 == True
	assert is_overlapping_player10 == True

	eggnemy_overlap_check6 = TestModel1.eggnemy_overlap_check(Boss2)
	eggnemy_overlap_check7 = TestModel2.eggnemy_overlap_check(Enemy3)
	eggnemy_overlap_check8 = TestModel3.eggnemy_overlap_check(Enemy2)
	eggnemy_overlap_check9 = TestModel4.eggnemy_overlap_check(Enemy1)
	eggnemy_overlap_check10 = TestModel5.eggnemy_overlap_check(Boss1)

	assert len(TestModel1.overlapping_player_eggnemy) == 0
	assert len(TestModel2.overlapping_player_eggnemy) == 0
	assert len(TestModel3.overlapping_player_eggnemy) == 1
	assert len(TestModel4.overlapping_player_eggnemy) == 2
	assert len(TestModel5.overlapping_player_eggnemy) == 2


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
	
	is_overlapping_player11 = TestModel1.is_overlapping_entities(Enemy1, TestModel1.player_egg)
	is_overlapping_player12 = TestModel2.is_overlapping_entities(Boss2, TestModel2.player_egg)
	is_overlapping_player13 = TestModel3.is_overlapping_entities(Enemy1, TestModel3.player_egg)
	is_overlapping_player14 = TestModel4.is_overlapping_entities(Boss1, TestModel4.player_egg)
	is_overlapping_player15 = TestModel5.is_overlapping_entities(Enemy1, TestModel2.player_egg)

	assert is_overlapping_player11 == False
	assert is_overlapping_player12 == False
	assert is_overlapping_player13 == False
	assert is_overlapping_player14 == False
	assert is_overlapping_player15 == False

	eggnemy_overlap_check11 = TestModel1.eggnemy_overlap_check(Enemy1)
	eggnemy_overlap_check12 = TestModel2.eggnemy_overlap_check(Boss2)
	eggnemy_overlap_check13 = TestModel3.eggnemy_overlap_check(Enemy3)
	eggnemy_overlap_check14 = TestModel4.eggnemy_overlap_check(Boss1)
	eggnemy_overlap_check15 = TestModel5.eggnemy_overlap_check(Enemy2)

	assert len(TestModel1.overlapping_player_eggnemy) == 0
	assert len(TestModel2.overlapping_player_eggnemy) == 0
	assert len(TestModel3.overlapping_player_eggnemy) == 1
	assert len(TestModel4.overlapping_player_eggnemy) == 1 #Since Boss1 does not overlap anymore, it is removed from the list of overlapping eggnemies.
	assert len(TestModel5.overlapping_player_eggnemy) == 2 #List of overlapping eggnemies remains unchanged since Enemy2 still overlaps.

	is_overlapping_player16 = TestModel1.is_overlapping_entities(Boss2, TestModel1.player_egg)
	is_overlapping_player17 = TestModel2.is_overlapping_entities(Enemy3, TestModel2.player_egg)
	is_overlapping_player18 = TestModel3.is_overlapping_entities(Enemy2, TestModel3.player_egg)
	is_overlapping_player19 = TestModel4.is_overlapping_entities(Enemy1, TestModel4.player_egg)
	is_overlapping_player20 = TestModel5.is_overlapping_entities(Boss1, TestModel5.player_egg)

	assert is_overlapping_player16 == False
	assert is_overlapping_player17 == False
	assert is_overlapping_player18 == False
	assert is_overlapping_player19 == True
	assert is_overlapping_player20 == False

	eggnemy_overlap_check16 = TestModel1.eggnemy_overlap_check(Boss2)
	eggnemy_overlap_check17 = TestModel2.eggnemy_overlap_check(Enemy3)
	eggnemy_overlap_check18 = TestModel3.eggnemy_overlap_check(Enemy2)
	eggnemy_overlap_check19 = TestModel4.eggnemy_overlap_check(Enemy1)
	eggnemy_overlap_check20 = TestModel5.eggnemy_overlap_check(Boss1)

	assert len(TestModel1.overlapping_player_eggnemy) == 0
	assert len(TestModel2.overlapping_player_eggnemy) == 0
	assert len(TestModel3.overlapping_player_eggnemy) == 0
	assert len(TestModel4.overlapping_player_eggnemy) == 1
	assert len(TestModel5.overlapping_player_eggnemy) == 1 #Since Boss1 does not overlap anymore, it is removed from list of overlapping eggnemies.

def test_restart():
	TestModel1.player_egg.stats.current_hp -= 451
	TestModel1.player_egg.stats.height += 482
	TestModel1.player_egg.stats.width += 127
	TestModel1.player_egg.stats.max_hp -= 329
	TestModel1.player_egg.stats.speed -= 32
	TestModel1.player_egg.center_position.x += 1231
	TestModel1.player_egg.center_position.y -= 100
	TestModel1.eggnemies.append(Boss1)
	TestModel1.overlapping_player_eggnemy.append(Enemy2)

	TestModel1.restart()

	assert len(TestModel1.eggnemies) == 0
	assert len(TestModel1.overlapping_player_eggnemy) == 0
	assert TestModel1.player_egg.stats.width == 20
	assert TestModel1.player_egg.stats.height == 40
	assert TestModel1.player_egg.stats.max_hp == 30
	assert TestModel1.player_egg.stats.current_hp == 30
	assert TestModel1.player_egg.stats.speed == 11

def test_game_finished():
	Point1 = deepcopy(TestPoint1)
	Point2 = deepcopy(TestPoint2)
	Point3 = deepcopy(TestPoint3)
	Point4 = deepcopy(TestPoint4)

	Point6 = Point(11.34, 2.12)
	Point7 = Point(7.64, 3.9)

	EggInfo2 = deepcopy(TestEggInfo2)

	EggInfo4 = deepcopy(TestEggInfo6)
	EggInfo5 = deepcopy(TestEggInfo7)
	EggInfo6 = deepcopy(TestEggInfo8)

	Player2 = PlayerEgg(EggInfo2, Point2, AtkRad2)

	Enemy1 = Eggnemy(EggInfo4, Point3)
	Enemy2 = Eggnemy(EggInfo5, Point1)
	Enemy3 = Eggnemy(EggInfo6, Point4)

	Settings1 = GameSettings(3, 200, 300, 100, 150)

	Model1 = deepcopy(TestModel1)
	Model2 = Model(Player2, Settings1, 3, TestEggInfo8, TestEggInfo9, 5, EgghancementSettings2)

	#Scenario 1: Game over due to no more hp.
	Model1.player_egg.stats.current_hp -= Model1.player_egg.stats.current_hp
	assert Model1.player_egg.stats.current_hp == 0
	Model1.update(True, True, False, False, True, None)
	assert Model1.is_game_over == True

	#Scenario 2: Tracking states before game over.
	Model2.player_egg.stats.current_hp -= 44
	Model2.overlapping_player_eggnemy.append(Enemy1)
	Model2.update(False, True, True, False, True, None)
	print(Model2.player_egg.stats.current_hp)
	assert Model2.frame_count == 1
	assert Model2.player_egg.stats.current_hp == 3

	Model2.overlapping_player_eggnemy.append(Enemy2)
	Model2.update(False, True, False, True, False, None)
	assert Model2.frame_count == 2
	assert Model2.player_egg.stats.current_hp == 3
	Model2.update(False, True, False, True, False, None)

	assert Model2.frame_count == 3
	Model2.overlapping_player_eggnemy.append(Enemy3)

	Model2.update(True, False, False, False, True, None)
	assert Model2.frame_count == 4
	assert Model2.player_egg.stats.current_hp == 0
	Model2.overlapping_player_eggnemy.remove(Enemy3)
	Model2.update(True, False, False, False, True, None) #It will only be game_over after this call since it needs to be updated.
	assert Model2.frame_count == 4
	assert Model2.is_game_over == True
	Model2.overlapping_player_eggnemy.remove(Enemy1)
	Model2.update(True, False, False, False, True, None)
	assert Model2.frame_count == 4
	assert Model2.is_game_over == True
		
def test_leaderboards():
	Model1 = deepcopy(TestModel1)
	
	Model1.update_leaderboards(12, 45)
	assert len(Model1.leaderboards_str) == 3
	assert len(Model1.leaderboards) == 1
	print(Model1.leaderboards)
	Model1.update_leaderboards(11, 63)
	print(Model1.leaderboards)
	assert Model1.leaderboards[0] == (12, 45)
	assert len(Model1.leaderboards) == 2
	assert len(Model1.leaderboards_str) == 3
	
	Model1.update_leaderboards(13, 23)
	assert Model1.leaderboards[0] == (13, 23)
	
	Model1.update_leaderboards(10, 53)
	assert len(Model1.leaderboards_str) == 3
	
	Model1.update_leaderboards(4, 1)
	assert Model1.leaderboards[2] == (11, 63)
	assert len(Model1.leaderboards) == 3
	
	Model1.update_leaderboards(30, 51)
	Model1.update_leaderboards(15, 3)
	Model1.update_leaderboards(2, 3)
	Model1.update_leaderboards(1, 2)
	Model1.update_leaderboards(3, 7)
	Filter1 = [*filter((lambda x: x == (13, 23)), Model1.leaderboards)]
	assert len(Filter1) == 1
	assert Model1.leaderboards[1] == (15, 3)
	Filter2 = [*filter((lambda x: x == (14, 15)), Model1.leaderboards)]
	assert len(Filter2) == 0
	Model1.update_leaderboards(15, 3)
	Filter3 = [*filter((lambda x: x == (15, 3)), Model1.leaderboards)]
	assert len(Filter3) == 2

test_game_finished()