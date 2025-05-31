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
    totalHp: S.Number,
    currentHp: S.Number,
    color: S.String,
    speed: S.Number,
    attackRange: S.Number,
    frameCountSinceLastDamaged: S.Option(S.Number),
    damage: S.Number,
})
export type PlayerEgg = typeof PlayerEgg.Type

export const Eggnemy = S.TaggedStruct("Eggnemy", {
    // yes, redundant but it may be more helpful to 
    // distinguish between the two later down the line
    centerCoords: Point,
    height: S.Number,
    width: S.Number,
    color: S.String,
    speed: S.Number,
    currentHp: S.Number,
    totalHp: S.Number,
    damage: S.Number,
})
export type Eggnemy = typeof Eggnemy.Type

export const Boss = S.TaggedStruct("Boss", {
    centerCoords: Point,
    height: S.Number,
    width: S.Number,
    color: S.String,
    speed: S.Number,
    currentHp: S.Number,
    totalHp: S.Number,
    damage: S.Number,
})
export type Boss = typeof Boss.Type

export const Egg = S.Union(
    PlayerEgg,
    Eggnemy,
    Boss,
)
export type Egg = typeof Egg.Type

export const BadEgg = S.Union(
    Eggnemy,
    Boss
)
export type BadEgg = typeof BadEgg.Type

export const Model = S.Struct({
    playerEgg: PlayerEgg,
    eggnemies: S.Array(Eggnemy),
    eggnemiesDefeated: S.Number,
    eggnemiesToKillBeforeBoss: S.Number,
    bosses: S.Array(Boss),
    fps: S.Int,
    isBossActive: S.Boolean,
    currentFrame: S.Int,
    timeInSeconds: S.Int,
    worldHeight: S.Number,
    worldWidth: S.Number,
    worldCenter: Point,
    worldBoundaryWidth: S.Number,
    screenHeight: S.Number,
    screenWidth: S.Number,
    gameState: S.Union(
        S.Literal("Ongoing"),
        S.Literal("PlayerWin"),
        S.Literal("PlayerLose")
    ),

    })
export type Model = typeof Model.Type

const Settings = S.Struct({
    fps: S.Number,
    screenWidth: S.Number,
    screenHeight: S.Number,
    worldWidth: S.Number,
    worldHeight: S.Number,
    worldBoundaryWidth: S.Number,

    playerEggHp: S.Number,
    playerEggWidth: S.Number,
    playerEggHeight: S.Number,
    playerEggRange: S.Number,
    playerEggSpeed: S.Number,

    initialEggnemyCount: S.Number,
    eggnemyWidth: S.Number,
    eggnemyHeight: S.Number,
    eggnemySpeed: S.Number,
    eggnemyInitialHp: S.Number,
    eggnemyDamage: S.Number,

    eggnemiesToKillBeforeBoss: S.Number,
    bossInitialHp: S.Number,
    bossWidth: S.Number,
    bossHeight: S.Number,
    bossSpeed: S.Number,
})
export type Settings = typeof Settings.Type

export const minsSecs = S.Struct({
    mins: S.Int,
    secs: S.Int,
})
export type minsSecs = typeof minsSecs.Type