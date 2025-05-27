import { Schema as S } from 'effect'

export const Point = S.Struct({
    x: S.Number,
    y: S.Number,
})
export type Point= typeof Point.Type

export const Egg = S.Struct({
    centerCoords: Point,
    height: S.Number,
    width: S.Number,
    total_hp: S.Number,
    current_hp: S.Number
})
export type Egg = typeof Egg.Type

export const Model = S.Struct({
    playerEgg: Egg,
    eggnemies: S.Array(Egg),
    fps: S.Int,
    currentFrame: S.Int
    })
export type Model = typeof Model.Type

const Settings = S.Struct({
    fps: S.Number,
    width: S.Number,
    height: S.Number,
    playerEggHp: S.Number,
    playerEggWidth: S.Number,
    playerEggHeight: S.Number,
    EggnemyCount: S.Number,
    EggnemyWidth: S.Number,
    EggnemyHeight: S.Number
})