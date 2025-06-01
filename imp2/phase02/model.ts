import { Array, Option, Schema as S } from 'effect'
import {
    PlayerEgg,
    Eggnemy,
    Boss,
    Point,
    minsSecs,
    settings
} from "./projectTypes"

export const Model = S.Struct({
    playerEgg: PlayerEgg,
    eggnemies: S.Array(Eggnemy),
    eggnemiesDefeated: S.Number,
    eggnemiesToKillBeforeBoss: S.Number,
    bosses: S.Array(Boss),
    fps: S.Int,
    isBossActive: S.Boolean,
    currentFrame: S.Int,
    currentTime: minsSecs,
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

export const playerEgg = PlayerEgg.make({
        centerCoords: Point.make({
            x: settings.screenWidth / 2,
            y: settings.screenHeight / 2,
        }),
        height: 20,
        width: 10,
        totalHp: 20,
        currentHp: 20,
        color: "white",
        speed: settings.playerEggSpeed,
        attackRange: settings.playerEggRange,
        frameCountSinceLastDamaged: Option.none(),
        damage: 3,
    })

export const initModel = Model.make({
        playerEgg: playerEgg,
        eggnemies: Array.make(
            Eggnemy.make({
                centerCoords: Point.make({x: 20, y: 20}),
                height: settings.eggnemyHeight,
                width: settings.eggnemyWidth,
                color: "gray",
                speed: settings.eggnemySpeed,
                currentHp: settings.eggnemyInitialHp,
                totalHp: settings.eggnemyInitialHp,
                damage: settings.eggnemyDamage
            }),
            Eggnemy.make({
                centerCoords: Point.make({x: 100, y: 250}),
                height: settings.eggnemyHeight,
                width: settings.eggnemyWidth,
                color: "gray",
                speed: settings.eggnemySpeed,
                currentHp: settings.eggnemyInitialHp,
                totalHp: settings.eggnemyInitialHp,
                damage: settings.eggnemyDamage
            }),
            Eggnemy.make({
                centerCoords: Point.make({x: 200, y: 200}),
                height: settings.eggnemyHeight,
                width: settings.eggnemyWidth,
                color: "gray",
                speed: settings.eggnemySpeed,
                currentHp: settings.eggnemyInitialHp,
                totalHp: settings.eggnemyInitialHp,
                damage: settings.eggnemyDamage
            }),
        ),
        bosses: Array.empty(),
        isBossActive: false,
        eggnemiesDefeated: 0,
        eggnemiesToKillBeforeBoss: settings.eggnemiesToKillBeforeBoss,
        worldHeight: settings.worldHeight,
        worldWidth: settings.worldWidth,
        worldCenter: Point.make({
            x: settings.screenWidth / 2,
            y: settings.screenHeight / 2,
        }),
        worldBoundaryWidth: settings.worldBoundaryWidth,
        screenHeight: settings.screenHeight,
        screenWidth: settings.screenWidth,
        fps: settings.fps,
        currentFrame: 0,
        currentTime: minsSecs.make({
            mins: 0,
            secs: 0,
        }),
        gameState: "Ongoing",
    })
