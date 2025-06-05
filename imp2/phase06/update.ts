import {Array, HashSet, Schema as S, pipe, Match, Option, Order, String } from 'effect'
import { Model, initModel } from "./model"
import {
    PlayerEgg,
    Egg,
    Eggnemy,
    Boss,
    BadEgg,
    BadEggsAndPoints,
    Msg,
    minsSecs,
    Point,
    EggUtils,
    settings,
} from "./projectTypes"

const shouldPlayerBeReceivingDamage = (model): boolean => 
    inContactWithBoss(model) || inContactWithEggnemy(model)

const inContactWithEggnemy = (model: Model): boolean =>
    Array.some(model.eggnemies, (eggnemy) => isInContact(model.playerEgg, eggnemy))

const inContactWithBoss = (model: Model): boolean => 
    Array.some(model.bosses, (boss) => isInContact(model.playerEgg, boss))
    

const spawnBoss = (model: Model) => 
    Model.make({
        ...model,
        bosses: Array.append(model.bosses, Boss.make({
            centerCoords: Point.make({
                x: Math.random() * model.screenWidth,
                y: Math.random() * model.screenHeight,
            }),
            height: settings.bossHeight,
            width: settings.bossWidth,
            color: "tan",
            currentHp: settings.bossInitialHp,
            totalHp: settings.bossInitialHp,
            attack: model.bossAttack,
            speed: model.bossSpeed,
        }) ),
        isBossActive: true,
        playerEgg: PlayerEgg.make({
            ...model.playerEgg,
            currentNetEggnemyKillsForBoss: (
                model.playerEgg.currentNetEggnemyKillsForBoss -
                model.eggnemiesToKillBeforeBoss
            )
        })
    })

const randomAddEggnemies = (eggnemies: readonly Eggnemy[], 
                            chance: number, model: Model): readonly Eggnemy[] => {
    if (Math.random() * 100 > chance) {
        return eggnemies
    }
    const numAdded = pipe(
        Math.random() * 10,
        Math.floor
    )
    let currentEggnemies = eggnemies
    for (let i = 0; i < numAdded; i++) {
        currentEggnemies = Array.append(currentEggnemies, Eggnemy.make({
            centerCoords: Point.make({
                x: Math.random() * settings.screenWidth,
                y: Math.random() * settings.screenHeight,
            }),
            height: settings.eggnemyHeight,
            width: settings.eggnemyWidth,
            color: "grey",
            speed: model.eggnemySpeed,
            currentHp: model.eggnemyHp,
            totalHp: model.eggnemyHp,
            attack: model.eggnemyAttack,
        }))
    }

    return currentEggnemies
}
    

const updateEggnemyKillCount = (model: Model, additionalCount) =>
    Model.make({
        ...model,
        eggnemiesDefeated: model.eggnemiesDefeated + additionalCount,
        playerEgg: PlayerEgg.make({
            ...model.playerEgg,
            currentNetExp: (
                model.playerEgg.currentNetExp + 
                additionalCount
            ),
            currentNetEggnemyKillsForBoss: (
                model.playerEgg.currentNetEggnemyKillsForBoss +
                additionalCount
            )
        })
    })

const getModelAfterEverythingMoved = (model: Model, key: string, distance: number) =>
    Model.make({
                ...model,
                eggnemies: pipe(
                    model.eggnemies,
                    Array.map((badEgg) => moveEggRelativeToPlayer(
                        badEgg, key, distance
                    ) as Eggnemy,   
                )),
                worldCenter: moveRelativeToPlayer(
                    model.worldCenter,
                    key,
                    distance,
                ),
                bosses: pipe(
                    model.bosses,
                    Array.map((boss) => moveEggRelativeToPlayer(
                        boss, key, distance
                    ) as Boss)
                )
            })

const moveEggRelativeToPlayer = (egg: BadEgg, key: string, distance: number) => 
    Match.value(egg).pipe(
        Match.tag('Eggnemy', (eggnemy) => 
            Eggnemy.make({
                        ...eggnemy,
                        centerCoords: moveRelativeToPlayer(
                            eggnemy.centerCoords,
                            key,
                            distance,
                        ),
                    })
        ),
        Match.tag("Boss", (boss) =>
            Boss.make({
                        ...boss,
                        centerCoords: moveRelativeToPlayer(
                            boss.centerCoords,
                            key,
                            distance,
                        ),
                    })
        ),
        Match.exhaustive
    )

const moveRelativeToPlayer = (point: Point, key: string, playerSpeed): Point =>
    key == 'w' || key == "ArrowUp"?     Point.make({...point, y: point.y + playerSpeed}) :
    key == 'a' || key == "ArrowLeft"?   Point.make({...point, x: point.x + playerSpeed}) :
    key == 's' || key == "ArrowDown"?   Point.make({...point, y: point.y - playerSpeed}) :
    key == 'd' || key == "ArrowRight"?  Point.make({...point, x: point.x - playerSpeed}) :
    point

function modelDamageToBadEggs(model: Model): Model {
    const updatedEggnemies = pipe(
            model.eggnemies,
            Array.map((eggnemy) => (takeDamageIfInRange(model.playerEgg, eggnemy)) as Eggnemy),
            Array.filter((eggnemy) => eggnemy.currentHp > 0),
        )
    const updatedBosses = pipe(
            model.bosses,
            Array.map((boss) => (takeDamageIfInRange(model.playerEgg, boss)) as Boss),
            Array.filter((boss) => boss.currentHp > 0)
        )

    return Model.make({
        ...model,
        eggnemies: updatedEggnemies,
        bosses: updatedBosses,
        didABossDie: (
            Array.length(updatedBosses) < Array.length(model.bosses)
        )
    })
}

const takeDamageIfInRange = (source: PlayerEgg, victim: BadEgg ) => 
    Match.value(victim).pipe(
        Match.tag('Eggnemy', (eggnemy) =>
            Eggnemy.make({
                ...eggnemy,
                currentHp: withinPlayerRange(source, eggnemy) ? 
                 Math.max(
                victim.currentHp - source.attack,
                0
            ) : eggnemy.currentHp
        })
        ),
        Match.tag("Boss", (boss) => 
        Boss.make({
            ...boss,
            currentHp: withinPlayerRange(source, boss) ? 
            Math.max(
                victim.currentHp - source.attack,
                0
            ) : boss.currentHp
        })

        ), Match.exhaustive)


const withinPlayerRange = (player: PlayerEgg, eggnemy: BadEgg): boolean =>
    // no specific definition as to what range was given
    (player.attackRange ** 2) >= 
    (player.centerCoords.x - eggnemy.centerCoords.x) ** 2 + 
    (player.centerCoords.y - eggnemy.centerCoords.y) ** 2 

const absDifference = (a: number, b: number): number =>
    Math.abs(a - b)

const isInContact = (egg1: Egg, egg2: Egg): boolean => 
    absDifference(egg1.centerCoords.x, egg2.centerCoords.x) < (egg1.width + egg2.width) / 2 &&
    absDifference(egg1.centerCoords.y, egg2.centerCoords.y) < (egg1.height + egg2.height) / 2
    

const returnPlayerToBounds = (model: Model): Model =>
    Model.make({
        ...model,
        worldCenter: (
            EggUtils.right(model.playerEgg)
            >= (model.worldCenter.x + model.worldWidth / 2) ?
            // to right   
            Point.make({...model.worldCenter, 
                        x: model.playerEgg.centerCoords.x - model.worldWidth / 2 
                        + model.playerEgg.width / 2
                    }) :
            EggUtils.left(model.playerEgg)
            <= (model.worldCenter.x - model.worldWidth / 2) ?
            Point.make({...model.worldCenter, 
                        x: model.playerEgg.centerCoords.x + model.worldWidth / 2  
                        - model.playerEgg.width / 2
                    }) :
            EggUtils.top(model.playerEgg)
            <= (model.worldCenter.y - model.worldHeight / 2) ?
            Point.make({...model.worldCenter, 
                        y: model.playerEgg.centerCoords.y + model.worldHeight / 2  
                        - model.playerEgg.height / 2
                    }) :
            EggUtils.bottom(model.playerEgg) 
            >= (model.worldCenter.y + model.worldHeight / 2) ?
            Point.make({...model.worldCenter, 
                        y: model.playerEgg.centerCoords.y - model.worldHeight / 2  
                        + model.playerEgg.height / 2
                    }) :
            model.worldCenter
        ),
    })

const isPlayerInBounds = (model: Model): boolean =>
    absDifference(model.worldCenter.x, model.playerEgg.centerCoords.x) + 
    model.playerEgg.width / 2 <= model.worldWidth / 2 &&
    absDifference(model.worldCenter.y, model.playerEgg.centerCoords.y) + 
    model.playerEgg.height / 2 <= model.worldHeight / 2

const isEggnemy = (egg: Egg): boolean =>
    Match.value(egg).pipe(
        Match.tag('Eggnemy', ()=> true),
        Match.orElse(() => false)
    )

const isBoss = (egg: Egg): boolean =>
    Match.value(egg).pipe(
        Match.tag("Boss", () => true),
        Match.orElse(() => false)
    )

    
export const update = (msg: Msg, model: Model): Model => 
    Match.value(msg).pipe(
        Match.tag("Canvas.MsgKeyDown", ({ key }) =>
            // pipe(console.log(model), () => false)? model :
            model.gameState === "ChoosingEgghancement"? 
            givePlayerEgghancement(model, key) :
            model.gameState != "Ongoing" && key == 'r'? Model.make({
                ...initModel,
                leaderboard: model.leaderboard,
                hasAddedToLeaderboard: false,
            }) :
            model.gameState == "GameOver" ? model : 
            (key == 'l' || key == 'L') ? 
            pipe(
                modelDamageToBadEggs(model),
                (newModel) => updateEggnemyKillCount(
                    newModel, absDifference(
                            Array.length(model.eggnemies),
                            Array.length(newModel.eggnemies)
                        )
                )      
            ) :
            pipe(
                getModelAfterEverythingMoved(model, key, model.playerEgg.speed),
                (model) =>  !isPlayerInBounds(model)? 
                            pipe(   
                                returnPlayerToBounds(model),
                                () => getModelAfterEverythingMoved(
                                    model, key, -model.playerEgg.speed
                                )): 
                            model
            )
        ),
        Match.tag('Canvas.MsgTick', () => 
            pipe(
            console.log(model.didABossDie),
            () => false
        ) ? model :
            // model.gameState !== "Ongoing"? model :
            model.gameState === "GameOver" ? model: // block input
            model.gameState === "ChoosingEgghancement" ? model :
            model.didABossDie ? pipe(
                console.log('bossDied'),
                () => updateBadEggStats(model)
            ) :
            model.playerEgg.currentHp <= 0?
            Model.make({...model, 
                gameState: "GameOver",
                leaderboard:    !model.hasAddedToLeaderboard?
                                pipe(
                                    Array.append(model.leaderboard, model.currentTime),
                                    Array.sortBy(
                                        Order.mapInput(Order.number, ({mins, secs}) => mins*60 + secs)
                                    ),
                                    Array.takeRight(3),
                                    Array.reverse
                                ):
                                model.leaderboard,
                hasAddedToLeaderboard: true,
            }):
            model.eggnemiesDefeated >= model.eggnemiesToKillBeforeBoss &&
            model.playerEgg.currentNetEggnemyKillsForBoss >= model.eggnemiesToKillBeforeBoss? // Array.isEmptyArray doesnt work for some reason
            spawnBoss(model) :
            // model.playerEgg.currentHp <= 0 ? Model.make({
            //     ...model,
            //     gameState: "GameOver",
            // }) :
            generalUpdate(model)
        ),
        Match.orElse(() => model)
    )

const updateBadEggStats = (model: Model) => Model.make({
    ...model,
    eggnemyAttack: model.eggnemyAttack + 1,
    eggnemyHp: model.eggnemyHp + 1,
    eggnemySpeed: model.eggnemySpeed + 1,
    bossAttack: model.bossAttack + 1,
    bossHp: model.bossHp * 1.5,
    bossSpeed: model.bossSpeed + 1,
    didABossDie: false,
})

const givePlayerEgghancement = (model: Model, key: string) =>
    Model.make({
        ...model,
        playerEgg: PlayerEgg.make({
            ...model.playerEgg,
            currentHp: key === "1"? model.playerEgg.currentHp + model.deltaHp : 
                        model.playerEgg.currentHp,
            totalHp: key === "1"? model.playerEgg.totalHp + model.deltaHp : 
                        model.playerEgg.totalHp,
            attack: key === "2"? model.playerEgg.attack + model.deltaAttack :
                        model.playerEgg.attack,
            speed: key === "3"? model.playerEgg.speed + model.deltaSpeed :
                        model.playerEgg.speed,
            currentNetExp: pipe(
                Array.make("1", "2", "3"),
                Array.contains(key),
                (isValidKey) => isValidKey?
                model.playerEgg.currentNetExp - model.eggxperienceNeededForEgghancement :
                model.playerEgg.currentNetExp
            )
        }),
        gameState: pipe(
            Array.make("1", "2", "3"),
            Array.contains(key),
            (isValidKey) => isValidKey? "Ongoing" : model.gameState
        )
    })

function generalUpdate(model: Model): Model {
    
    const totalSeconds = Math.floor(model.currentFrame / model.fps)
    const newTime = minsSecs.make({
                    mins: Math.floor(totalSeconds / 60),
                    secs: totalSeconds % 60,
                })
    const newFrame = model.currentFrame + 1
    let newPlayerHp: number

    const hasCollided = shouldPlayerBeReceivingDamage(model)
    if (hasCollided) {
        newPlayerHp = Match.value(model.playerEgg.frameCountSinceLastDamaged).pipe(
                        Match.tag("None", () => model.playerEgg.currentHp),
                            // if we decrement immediately after a new collision, the next tick will
                            // decrement as well, leading to a double decrement
                        Match.tag("Some", (frameCountSinceLastDamaged) => (
                            // if more than one frame has passed since last dmg, decrement 1
                            frameCountSinceLastDamaged.value < model.fps? 
                            model.playerEgg.currentHp : 
                            inContactWithBoss(model) && inContactWithEggnemy(model)?
                            model.playerEgg.currentHp - (
                                // contact with boss AND normal eggnemy 
                                model.bossAttack + model.eggnemyAttack
                            ) : 
                            inContactWithBoss(model)? 
                            model.playerEgg.currentHp - model.bossAttack :  
                            model.playerEgg.currentHp - model.eggnemyAttack

                        )),
                        Match.exhaustive,
                    )
    } else {
        newPlayerHp = model.playerEgg.currentHp
    }
    // console.log(
    //     model.gameState,
    //     model.playerEgg.currentNetExp,
    //     model.eggxperienceNeededForEgghancement
    // )
    return Model.make({
        ...model,
        gameState: model.playerEgg.currentNetExp >= model.eggxperienceNeededForEgghancement?
                    "ChoosingEgghancement" : model.gameState,
        currentTime: newTime,
        currentFrame: newFrame,
        playerEgg: PlayerEgg.make({
            ...model.playerEgg,
            currentHp: newPlayerHp,
            frameCountSinceLastDamaged: Match.value(model.playerEgg.frameCountSinceLastDamaged).pipe(
                Match.tag('None', () => hasCollided? Option.some(0): Option.none()),
                Match.tag("Some", (countOption) =>  countOption.value < model.fps? 
                                                    Option.some(countOption.value + 1):
                                                    Option.none()
                ),
                Match.exhaustive
            ),
            eggxperience: model.eggnemiesDefeated
        }),
        eggnemies: pipe(
            moveEntities(model.eggnemies, model.playerEgg) as Eggnemy[],
            (eggArr) => Array.length(model.eggnemies) < settings.initialEggnemyCount?
                randomAddEggnemies(eggArr, 5, model) : eggArr
        ),
        bosses: moveEntities(model.bosses, model.playerEgg) as Boss[]
    })
}

function moveEntities(eggnemies: readonly Egg[], target: PlayerEgg): Egg[] {
    return moveEntitiesHelper(eggnemies, 0, Array.empty(), target)
}

function moveEntitiesHelper(eggnemies: readonly Egg[], idx: number, 
                            ret: Egg[], target: PlayerEgg): Egg[] {
    if (idx == Array.length(eggnemies)) {
        return ret
    }

    const currEntity = Array.unsafeGet(eggnemies, idx)
    const nextPoint = stepOnce(currEntity, target)

    const isNextPointOccupied: boolean = pipe(
        ret,
        // Array.map((eggnemy) => eggnemy.centerCoords),
        // Array.some(({x, y}) => x == nextPoint.x && y == nextPoint.y)
        Array.some((entity) => isInContact(entity, currEntity))
    )
    const updatedEntity: Egg = Match.value(currEntity).pipe(
        Match.tag("Boss", (boss) => Boss.make({
            ...boss,
            centerCoords: isNextPointOccupied? boss.centerCoords : nextPoint
        })),
        Match.tag("Eggnemy", (eggnemy) => Eggnemy.make({
        ...eggnemy,
        centerCoords: isNextPointOccupied? eggnemy.centerCoords : nextPoint
        })),
        Match.tag("PlayerEgg", (player) => PlayerEgg.make({
            // SHOULD NOT REACH HERE, but may prove useful later
            ...player,
            centerCoords: isNextPointOccupied? player.centerCoords : nextPoint
        })),
        Match.exhaustive,
    )

    const updatedRet = Array.append(ret, updatedEntity)

    return moveEntitiesHelper(eggnemies, idx + 1, updatedRet, target)
}

const stepOnce = (egg: Egg, target: Egg): Point =>
    Point.make({
        x:  egg.centerCoords.x < target.centerCoords.x? egg.centerCoords.x + egg.speed :
            egg.centerCoords.x > target.centerCoords.x? egg.centerCoords.x - egg.speed :
            egg.centerCoords.x,
        y:  egg.centerCoords.y < target.centerCoords.y? egg.centerCoords.y + egg.speed :
            egg.centerCoords.y > target.centerCoords.y? egg.centerCoords.y - egg.speed :
            egg.centerCoords.y,    
    })

