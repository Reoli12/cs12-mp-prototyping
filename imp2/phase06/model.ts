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
    eggnemySpeed: S.Number,
    eggnemyAttack: S.Number,
    eggnemyHp: S.Number,
    
    bosses: S.Array(Boss),
    bossSpeed: S.Number,
    bossAttack: S.Number,
    bossHp: S.Number,
    isBossActive: S.Boolean,

    fps: S.Int,
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
        S.Literal("GameOver"),
        S.Literal("ChoosingEgghancement")
    ),
    leaderboard: S.Array(minsSecs),
    hasAddedToLeaderboard: S.Boolean,

    eggxperienceNeededForEgghancement: S. Number,
    deltaHp: S. Number,
    deltaAttack: S. Number,
    deltaSpeed: S. Number,
    didABossDie: S.Boolean,
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
        attack: 1,
        eggxperience: 0,
        currentNetExp: 0,
        currentNetEggnemyKillsForBoss: 0,
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
        eggxperienceNeededForEgghancement: settings.eggxperienceNeededForEgghancement,
        deltaAttack: settings.deltaAttack,
        deltaHp: settings.deltaHp,
        deltaSpeed: settings.deltaSpeed,
        bossAttack: settings.bossInitialAttack,
        bossSpeed: settings.bossInitialSpeed,
        bossHp: settings.bossInitialHp,
        eggnemyAttack: settings.eggnemyInitialAttack,
        eggnemySpeed: settings.eggnemyInitialSpeed,
        eggnemyHp: settings.eggnemyInitialHp,
        didABossDie: false,
    })

export function generateInitialEggnemies(num: number): Eggnemy[] {
    let ret: Eggnemy[] = Array.empty()
    for (let i = 0; i < num; i++) {
        ret = Array.append(ret, Eggnemy.make({
            centerCoords: Data.struct({
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
            speed: settings.eggnemyInitialSpeed,
            attack: settings.eggnemyInitialAttack,
            currentHp: settings.eggnemyInitialHp,
            totalHp: settings.eggnemyInitialHp,
        }))
    }
    return ret
}
