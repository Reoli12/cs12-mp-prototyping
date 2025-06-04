import { Array, HashSet, Option, pipe, Schema as S, Data  } from 'effect'
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
    leaderboard: S.Array(minsSecs),
    hasAddedToLeaderboard: S.Boolean,
    occupiedPoints: S.HashSet(Point),
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

const initEggnemies = generateInitialEggnemies(settings.initialEggnemyCount)

export const initModel = Model.make({
        playerEgg: playerEgg,
        eggnemies: initEggnemies,
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
        leaderboard: Array.empty(),
        hasAddedToLeaderboard: false,
        occupiedPoints: pipe(
            initEggnemies,
            Array.map((eggnemy) => eggnemy.centerCoords),
            HashSet.fromIterable
        )
    })

function generateInitialEggnemies(num: number): Eggnemy[] {
    let ret: Eggnemy[] = Array.empty()
    for (let i = 0; i < num; i++) {
        ret = Array.append(ret, Eggnemy.make({
            centerCoords: Point.make({
                x: pipe( 
                    Math.random() * settings.screenWidth,
                    Math.floor
                    ),
                y: pipe(
                    Math.random() * settings.screenHeight,
                    Math.floor
                )
            }),
            height: settings.eggnemyHeight,
            width: settings.eggnemyWidth,
            color: "gray",
            speed: settings.eggnemySpeed,
            damage: 1,
            currentHp: settings.eggnemyInitialHp,
            totalHp: settings.eggnemyInitialHp,
        }))
    }
    return ret
}
