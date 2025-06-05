import { Schema as S } from 'effect'
import { CanvasMsg, canvasView } from "cs12242-mvu/src/canvas"
import * as Canvas from "cs12242-mvu/src/canvas"

import data from "./settings.json" 
export const settings = data as unknown as Settings // idk why but ts says to convert as unknwon first


export const playerSpriteSrc = "/resources/player.png"
export const eggnemySpriteSrc = "/resources/eggnemy.png"
export const bossSpriteSrc = "/resources/boss.png"

export type Msg = typeof CanvasMsg.Type // update strictly only takes in Msg

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
    color: S.String,
    attackRange: S.Number,
    frameCountSinceLastDamaged: S.Option(S.Number),
    attack: S.Number,
    totalHp: S.Number,
    currentHp: S.Number,
    speed: S.Number,
    eggxperience: S.Number,
    currentNetExp: S.Number,
    currentNetEggnemyKillsForBoss: S.Number,
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
    attack: S.Number,
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
    attack: S.Number,
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

export const minsSecs = S.Struct({
    mins: S.Int,
    secs: S.Int,
})
export type minsSecs = typeof minsSecs.Type

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
    eggnemyInitialSpeed: S.Number,
    eggnemyInitialHp: S.Number,
    eggnemyInitialAttack: S.Number,

    eggnemiesToKillBeforeBoss: S.Number,
    bossInitialHp: S.Number,
    bossWidth: S.Number,
    bossHeight: S.Number,
    bossInitialSpeed: S.Number,
    bossInitialAttack: S.Number,

    eggxperienceNeededForEgghancement: S. Number,
    deltaHp: S. Number,
    deltaAttack: S. Number,
    deltaSpeed: S. Number,

})
export type Settings = typeof Settings.Type

export const getLeft = (egg: Egg) =>
    egg.centerCoords.x - egg.width / 2

export const getRight = (egg: Egg) => 
    egg.centerCoords.x + egg.width / 2

export const getTop = (egg: Egg) =>
    egg.centerCoords.y - egg.height / 2

export const getBottom = (egg: Egg) => 
    egg.centerCoords.y + egg.height / 2

export const EggUtils = {
    // required to use effect, but no where does it say that were not allowed to use
    // regular js
    top: getTop,
    bottom: getBottom,
    left: getLeft,
    right: getRight,
}

export const BadEggsAndPoints = S.Struct({
    eggnemies: S.Array(Eggnemy),
    bosses: S.Array(Boss),
    points: S.HashSet(Point)
})
export type BadEggsAndPoints = typeof BadEggsAndPoints.Type
