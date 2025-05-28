import { Schema as S } from 'effect'

export const EggSides = S.Union(
    S.Literal("top"),
    S.Literal("bottom"),
    S.Literal("left"),
    S.Literal("right"),
)
export type EggSides = typeof EggSides.Type

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
    current_hp: S.Number,
    color: S.String,
    speed: S.Number
})
export type Egg = typeof Egg.Type

export const Eggnemy = S.Struct({
    // yes, redundant but it may be more helpful to 
    // distinguish between the two later down the line
    centerCoords: Point,
    height: S.Number,
    width: S.Number,
    total_hp: S.Number,
    current_hp: S.Number,
    color: S.String,
    speed: S.Number
})
export type Eggnemy = typeof Eggnemy.Type

export const Model = S.Struct({
    playerEgg: Egg,
    eggnemies: S.Array(Eggnemy),
    fps: S.Int,
    currentFrame: S.Int,
    worldHeight: S.Number,
    worldWidth: S.Number,

    })
export type Model = typeof Model.Type

const Settings = S.Struct({
    fps: S.Number,
    width: S.Number,
    height: S.Number,
    PlayerEggHp: S.Number,
    PlayerEggWidth: S.Number,
    PlayerEggHeight: S.Number,
    EggnemyCount: S.Number,
    EggnemyWidth: S.Number,
    EggnemyHeight: S.Number,
    PlayerEggSpeed: S.Number,
    EggnemySpeed: S.Number,
})
export type Settings = typeof Settings.Type