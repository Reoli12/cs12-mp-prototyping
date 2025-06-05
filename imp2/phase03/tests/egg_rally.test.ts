import {generateInitialEggnemies, Model} from "../model"
import {
    PlayerEgg,
    Eggnemy,
    Boss,
    Point,
    minsSecs,
    settings,
    getLeft,
    getRight,
    getTop,
    getBottom
} from "../projectTypes"
import {
	inContactWithEggnemy,
	inContactWithBoss,
	shouldPlayerBeReceivingDamage,
	spawnBoss,
	randomAddEggnemies,
	updateEggnemyKillCount,
	withinPlayerRange,
	takeDamage,
	moveEggRelativeToPlayer,
} from "../update"
import {Option, Array, Schema as S } from 'effect'
import {describe, expect, it} from 'vitest'

const PlayerEgg1 = PlayerEgg.make({
	centerCoords: Point.make({
		x: 32,
		y: -4,
	}),	
	height: 20,
	width: 10,
	totalHp: 30,
	currentHp: 20,
	color: "blue",
	speed: 20,
	attackRange: 5,
	frameCountSinceLastDamaged: Option.none(),
	damage: 4
	})

const Eggnemy1 = Eggnemy.make({
	centerCoords: Point.make({
		x: 10,
		y: -2.368,
	}),	
	height: 10,
    width: 20,
    color: "green",
    speed: 5,
    currentHp: 10,
    totalHp: 15,
    damage: 2,
	})

const Boss1 = Boss.make({
	centerCoords: Point.make({
		x: 35,
		y: -5.61,
	}),	
	height: 30,
    width: 40,
    color: "green",
    speed: 5,
    currentHp: 40,
    totalHp: 45,
    damage: 5,
	})

const Model1 = Model.make({
    playerEgg: PlayerEgg1,
    eggnemies: Array.make(Eggnemy1),
    eggnemiesDefeated: 0,
    eggnemiesToKillBeforeBoss: 7,   
    bosses: Array.make(Boss1),
    fps: 30,
    isBossActive: false,
    currentFrame: 1,
    currentTime: minsSecs.make({
    	mins: 0,
    	secs: 5,
    }),
    worldHeight: 300,
    worldWidth: 300,
    worldCenter: Point.make({
		x: 0,
		y: 3,
	}),
    worldBoundaryWidth: 50,
    screenHeight: 200,
    screenWidth: 200,
    gameState: "Ongoing",
    leaderboard: Array.empty(),
    hasAddedToLeaderboard: false,
})

const Model2 = Model.make({
     playerEgg: PlayerEgg1,
    eggnemies: Array.make(Eggnemy1),
    eggnemiesDefeated: 0,
    eggnemiesToKillBeforeBoss: 7,   
    bosses: Array.make(Boss1),
    fps: 30,
    isBossActive: false,
    currentFrame: 1,
    currentTime: minsSecs.make({
    	mins: 0,
    	secs: 5,
    }),
    worldHeight: 300,
    worldWidth: 300,
    worldCenter: Point.make({
		x: 0,
		y: 3,
	}),
    worldBoundaryWidth: 50,
    screenHeight: 200,
    screenWidth: 200,
    gameState: "PlayerWin",
    leaderboard: Array.empty(),
    hasAddedToLeaderboard: false,
})

const spawnBoss1 = spawnBoss(Model1)
const addEggnemies1 = randomAddEggnemies(Model1.eggnemies, 45, Model1)
const updateKillCount1 = updateEggnemyKillCount(Model1, 9)
const updateKillCount2 = updateEggnemyKillCount(updateKillCount1, 9)
const withinPlayerRange1 = withinPlayerRange(Model1.playerEgg, Model1.eggnemies[0])
const withinPlayerRange2 = withinPlayerRange(Model1.playerEgg, Model1.bosses[0])
const takeDamage1 = takeDamage(Model1.playerEgg, Model1.eggnemies[0])
const takeDamage2 = takeDamage(Model1.playerEgg, Model1.bosses[0])
const moveRelativeToPlayer1 = moveEggRelativeToPlayer(Model1.eggnemies[0], "w", 6)
const moveRelativeToPlayer2 = moveEggRelativeToPlayer(Model2.bosses[0], "d", 6)

describe('#getLeft', () => {
	it('works for players', () => {
		expect(getLeft(PlayerEgg1)).toStrictEqual(27)
	})

	it('works for eggnemies', () => {
		expect(getLeft(Eggnemy1)).toStrictEqual(0)
	})

	it('works for bosses', () => {
		expect(getLeft(Boss1)).toStrictEqual(15)
	})
})

describe('#getRight', () => {
	it('works for players', () => {
		expect(getRight(PlayerEgg1)).toStrictEqual(37)
	})

	it('works for eggnemies', () => {
		expect(getRight(Eggnemy1)).toStrictEqual(20)
	})
	
	it('works for bosses', () => {
		expect(getRight(Boss1)).toStrictEqual(55)
	})
})

describe('#getTop', () => {
	it('works for players', () => {
		expect(getTop(PlayerEgg1)).toStrictEqual(-14)
	})

	it('works for eggnemies', () => {
		expect(getTop(Eggnemy1)).toStrictEqual(-7.368)
	})
	
	it('works for bosses', () => {
		expect(getTop(Boss1)).toStrictEqual(-20.61)
	})
})

describe('#getTop', () => {
	it('works for players', () => {
		expect(getBottom(PlayerEgg1)).toStrictEqual(6)
	})

	it('works for eggnemies', () => {
		expect(getBottom(Eggnemy1)).toStrictEqual(2.632)
	})
	
	it('works for bosses', () => {
		expect(getBottom(Boss1)).toStrictEqual(9.39)
	})
})

describe('#generateInitialEggnemies', () => {
	it('returns an array containing a list of eggnemies', () => {
		expect(generateInitialEggnemies(7)).toHaveLength(7)
	})
})

describe('#inContactWithEggnemy', () => {
	it('should return false here', () => {
		expect(inContactWithEggnemy(Model1)).toStrictEqual(false)
	})
})

describe('#inContactWithBoss', () => {
	it('should return true here', () => {
		expect(inContactWithBoss(Model1)).toStrictEqual(true)
	})
})

describe('#shouldPlayerBeReceivingDamage', () => {
	it('should return true here', () => {
		expect(shouldPlayerBeReceivingDamage(Model1)).toStrictEqual(true)
	})
})

describe('#withinPlayerRange', () => {
	it('should return true', () => {
		expect(withinPlayerRange1).toBe(false)
	})

	it('should return true', () => {
		expect(withinPlayerRange2).toBe(true)
	})
})

describe('#takeDamageIfInRange', () => {
	it('should not decrease the currentHp', () => {
		expect(takeDamage1.currentHp).toBe(6)
	})

	it('should decrease the currentHp', () => {
		expect(takeDamage2.currentHp).toBe(36)
	})
})

describe('#moveEggRelativeToPlayer', () => {
	it('should not move the x-coordinate here', () => {
		expect(moveRelativeToPlayer1.centerCoords.x).toBe(10)
	})

	it('should move the y-coordinate here', () => {
		expect(moveRelativeToPlayer1.centerCoords.y).toBe(3.632)
	})

	it('should move the x-coordinate here', () => {
		expect(moveRelativeToPlayer2.centerCoords.x).toBe(29)
	})

	it('should not move the y-coordinate here', () => {
		expect(moveRelativeToPlayer2.centerCoords.y).toBe(-5.61)
	})
})

describe('#bossSpawn', () => {
	it('increases number of bosses in Model.bosses', () => {
		expect(spawnBoss1.bosses).toHaveLength(2)
	})
})

describe('#randomAddEggnemies', () => {
	it('increases number of bosses in Model.bosses', () => {
		expect(Array.length(addEggnemies1)).toBeGreaterThanOrEqual(1)
	})
})

describe('#updateEggnemyKillCount', () => {
	it('increases eggnemiesDefeated of model', () => {
		expect(updateKillCount1.eggnemiesDefeated).toBe(9)
	})

	it('increases eggnemiesDefeated of model', () => {
		expect(updateKillCount2.eggnemiesDefeated).toBe(18)
	})
})
