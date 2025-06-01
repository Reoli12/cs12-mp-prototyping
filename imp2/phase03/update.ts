import {Array, Schema as S, pipe, Match, Option, String } from 'effect'
import { Model, initModel } from "./model"
import {
    PlayerEgg,
    Egg,
    Eggnemy,
    Boss,
    BadEgg,
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
            damage: 3,
            speed: settings.bossSpeed,
        }) ),
        isBossActive: true
    })

const randomAddEggnemies = (eggnemies: Eggnemy[], chance: number): Eggnemy[] => {
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
            speed: settings.eggnemySpeed,
            currentHp: settings.eggnemyInitialHp,
            totalHp: settings.eggnemyInitialHp,
            damage: settings.eggnemyDamage
        }))
    }

    return currentEggnemies
}
    

const updateEggnemyKillCount = (model: Model, additionalCount) =>
    Model.make({
        ...model,
        eggnemiesDefeated: model.eggnemiesDefeated + additionalCount
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
                    String.toLowerCase(key),
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
                            String.toLowerCase(key),
                            distance,
                        ),
                    })
        ),
        Match.tag("Boss", (boss) =>
            Boss.make({
                        ...boss,
                        centerCoords: moveRelativeToPlayer(
                            boss.centerCoords,
                            String.toLowerCase(key),
                            distance,
                        ),
                    })
        ),
        Match.exhaustive
    )

const moveRelativeToPlayer = (point: Point, key: string, playerSpeed): Point =>
    key == 'w' ? Point.make({...point, y: point.y + playerSpeed}) :
    key == 'a' ? Point.make({...point, x: point.x + playerSpeed}) :
    key == 's' ? Point.make({...point, y: point.y - playerSpeed}) :
    key == 'd' ? Point.make({...point, x: point.x - playerSpeed}) :
    point

const modelDefeatedEggnemies = (model: Model): Model => 
    Model.make({
        ...model,
        eggnemies: Array.map(model.eggnemies, 
            (eggnemy) => (withinPlayerRange(model.playerEgg, eggnemy) ?
                         takeDamage(model.playerEgg, eggnemy):
                         eggnemy) as Eggnemy
        )
    }) 

const modelDamageToBadEggs = (model: Model): Model =>
    Model.make({
        ...model,
        eggnemies: pipe(
            model.eggnemies,
            Array.map((eggnemy) => (takeDamage(model.playerEgg, eggnemy)) as Eggnemy),
            Array.filter((eggnemy) => eggnemy.currentHp > 0),
        ),
        bosses: pipe(
            model.bosses,
            Array.map((boss) => (takeDamage(model.playerEgg, boss)) as Boss),
            Array.filter((boss) => boss.currentHp > 0)
        )
        ,
    })

const takeDamage = (source: PlayerEgg, victim: BadEgg ) => 
    Match.value(victim).pipe(
        Match.tag('Eggnemy', (eggnemy) =>
            Eggnemy.make({
                ...eggnemy,
                currentHp: Math.max(
                victim.currentHp - source.damage,
                0
            )})
        ),
        Match.tag("Boss", (boss) => 
        Boss.make({
            ...boss,
            currentHp: Math.max(
                victim.currentHp - source.damage,
                0
            )})

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


const getNewEggnemyCoords = (eggnemyCoords: Point, playerEggCoords: Point, eggnemySpeed: number): Point => 
    Point.make({
        x:  eggnemyCoords.x < playerEggCoords.x? eggnemyCoords.x + eggnemySpeed :
            eggnemyCoords.x > playerEggCoords.x? eggnemyCoords.x - eggnemySpeed :
            eggnemyCoords.x,
        y:  eggnemyCoords.y < playerEggCoords.y? eggnemyCoords.y + eggnemySpeed :
            eggnemyCoords.y > playerEggCoords.y? eggnemyCoords.y - eggnemySpeed :
            eggnemyCoords.y,
    })

    

export const update = (msg: Msg, model: Model): Model => 
    Match.value(msg).pipe(
        Match.tag("Canvas.MsgKeyDown", ({ key }) =>
            // pipe(console.log(model), () => false)? model :
            model.gameState != "Ongoing" && key == 'r'? initModel :
            model.gameState != "Ongoing"? model : 
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
            model.isBossActive && Array.length(model.bosses) === 0?
            Model.make({...model, gameState: "PlayerWin"}):
            model.eggnemiesDefeated >= model.eggnemiesToKillBeforeBoss &&
            Array.length(model.bosses) === 0? // Array.isEmptyArray doesnt work for some reason
            spawnBoss(model) :
            model.playerEgg.currentHp <= 0 ? Model.make({
                ...model,
                gameState: "PlayerLose",
            }) :
            // !isPlayerInBounds(model)?
            // returnPlayerToBounds(model):
            model.gameState !== "Ongoing"? model :
            shouldPlayerBeReceivingDamage(model) ? Model.make({
                // with collision
                ...model,
                playerEgg: PlayerEgg.make({
                    ...model.playerEgg,
                    currentHp: Match.value(model.playerEgg.frameCountSinceLastDamaged).pipe(
                        Match.tag("None", () => model.playerEgg.currentHp),
                            // if we decrement immediately after a new collision, the next tick will
                            // decrement as well, leading to a double decrement
                        Match.tag("Some", (frameCountSinceLastDamaged) => (
                            // if more than one frame has passed since last dmg, decrement 1
                            frameCountSinceLastDamaged.value < model.fps? 
                            model.playerEgg.currentHp : 
                            inContactWithBoss(model) && inContactWithEggnemy(model)?
                            model.playerEgg.currentHp -4 : // contact with boss AND normal eggnemy 
                            inContactWithBoss(model)? 
                            model.playerEgg.currentHp - 3 :  
                            model.playerEgg.currentHp - 1

                        )),
                        Match.exhaustive,
                    ),
                    frameCountSinceLastDamaged: Match.value(model.playerEgg.frameCountSinceLastDamaged).pipe(
                        Match.tag("None", () => Option.some(model.fps)),
                        Match.tag("Some", (frameCount) => 
                            frameCount.value < model.fps? Option.some(frameCount.value + 1) : Option.some(0)
                            // since egg is damaged here, update count to 0
                        ), 
                        Match.exhaustive
                    )
            }),
            eggnemies: Array.map(model.eggnemies, (eggnemy) => 
                Eggnemy.make({
                    ...eggnemy,
                    centerCoords: getNewEggnemyCoords(eggnemy.centerCoords, model.playerEgg.centerCoords, eggnemy.speed)
                })
            ),
            bosses: Array.map(model.bosses, (boss) => Boss.make({
                ...boss,
                centerCoords: getNewEggnemyCoords(boss.centerCoords, model.playerEgg.centerCoords, boss.speed)
            })),
            }) : Model.make({
                // no collision 
                ...model,
                currentTime: minsSecs.make({
                    mins: Math.floor(model.currentTime.secs / 60),
                    secs: model.currentFrame % model.fps == 0? model.currentTime.secs + 1 : model.currentTime.secs ,
                }),
                currentFrame: model.currentFrame + 1,
                playerEgg: PlayerEgg.make({
                    ...model.playerEgg,
                    frameCountSinceLastDamaged: Match.value(model.playerEgg.frameCountSinceLastDamaged).pipe(
                        Match.tag("None", () => Option.none()),
                        Match.tag("Some", (frameCount) => 
                            frameCount.value < model.fps? Option.some(frameCount.value + 1) :
                            Option.none()
                    ),
                    Match.exhaustive
                )
                }),
                    eggnemies: pipe(
                        model.eggnemies,
                        Array.map((eggnemy) => Eggnemy.make({
                            ...eggnemy,
                            centerCoords: getNewEggnemyCoords(eggnemy.centerCoords, 
                                model.playerEgg.centerCoords, eggnemy.speed)
                        })),
                        (movedEggnemies) => randomAddEggnemies(movedEggnemies, 2)
            ),
                    bosses: Array.map(model.bosses, (boss) => Boss.make({
                        ...boss,
                        centerCoords: getNewEggnemyCoords(boss.centerCoords, model.playerEgg.centerCoords, boss.speed)
            }))
                
            }),
        ),
        Match.orElse(() => model)
    )