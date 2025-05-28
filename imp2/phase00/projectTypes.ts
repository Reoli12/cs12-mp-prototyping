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

export const PlayerEgg = S.TaggedStruct("PlayerEgg", {
    centerCoords: Point,
    height: S.Number,
    width: S.Number,
    total_hp: S.Number,
    current_hp: S.Number,
    color: S.String,
    speed: S.Number
})
export type PlayerEgg = typeof PlayerEgg.Type

export const Eggnemy = S.TaggedStruct("Eggnemy", {
    // yes, redundant but it may be more helpful to 
    // distinguish between the two later down the line
    centerCoords: Point,
    height: S.Number,
    width: S.Number,
    color: S.String,
    speed: S.Number
})
export type Eggnemy = typeof Eggnemy.Type

export const Egg = S.Union(
    PlayerEgg,
    Eggnemy,
)
export type Egg = typeof Egg.Type

export const Model = S.Struct({
    playerEgg: PlayerEgg,
    eggnemies: S.Array(Eggnemy),
    fps: S.Int,
    currentFrame: S.Int,
    worldHeight: S.Number,
    worldWidth: S.Number,
    isOver: S.Boolean,
    })
export type Model = typeof Model.Type

const Settings = S.Struct({
    fps: S.Number,
    width: S.Number,
    height: S.Number,
    playerEggHp: S.Number,
    playerEggWidth: S.Number,
    playerEggHeight: S.Number,
    eggnemyCount: S.Number,
    eggnemyWidth: S.Number,
    eggnemyHeight: S.Number,
    playerEggSpeed: S.Number,
    eggnemySpeed: S.Number,
})
export type Settings = typeof Settings.Type