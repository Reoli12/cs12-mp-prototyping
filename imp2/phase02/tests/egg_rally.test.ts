import {generateInitialEggnemies} from "../model"
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

describe('#getLeft', () => {
	it('works for a combination of positive and negative integers', () => {
		expect(getLeft(PlayerEgg1)).toStrictEqual(27)
	})
})

describe('#getRight', () => {
	it('works for a combination of positive and negative integers', () => {
		expect(getRight(PlayerEgg1)).toStrictEqual(37)
	})
})

describe('#getTop', () => {
	it('works for a combination of positive and negative integers', () => {
		expect(getTop(PlayerEgg1)).toStrictEqual(-14)
	})
})

describe('#getTop', () => {
	it('works for a combination of positive and negative integers', () => {
		expect(getBottom(PlayerEgg1)).toStrictEqual(6)
	})
})

describe('#generateInitialEggnemies', () => {
	it('returns an array containing a list of eggnemies', () => {
		expect(generateInitialEggnemies(7)).toHaveLength(7)
	})
})