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
            damage: 3,
            speed: settings.bossSpeed,
        }) ),
        isBossActive: true
    })

const randomAddEggnemies = (eggnemies: readonly Eggnemy[], chance: number): readonly Eggnemy[] => {
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

function modelDamageToBadEggs(model: Model): Model {
    const updatedEggnemies = pipe(
            model.eggnemies,
            Array.map((eggnemy) => (takeDamage(model.playerEgg, eggnemy)) as Eggnemy),
            Array.filter((eggnemy) => eggnemy.currentHp > 0),
        )
    const updatedBosses = pipe(
            model.bosses,
            Array.map((boss) => (takeDamage(model.playerEgg, boss)) as Boss),
            Array.filter((boss) => boss.currentHp > 0)
        )
    // let currentlyOccupiedPoints = model.occupiedPoints

    // let updatedEggnemies = Array.empty()
    // for (const eggnemy of model.eggnemies) {
    //     const eggnemyDamaged = takeDamage(model.playerEgg, eggnemy)
    //     if (eggnemyDamaged.currentHp >= 0) {
    //         HashSet.remove(currentlyOccupiedPoints, eggnemyDamaged.centerCoords)
    //     } else {
    //         Array.append(updatedEggnemies, eggnemyDamaged)
    //         HashSet.add(currentlyOccupiedPoints, eggnemyDamaged.centerCoords)
    //     }
    // }

    // let updatedBosses = Array.empty()
    // for (const boss of model.eggnemies) {
    //     const bossDamaged = takeDamage(model.playerEgg, boss)
    //     if (bossDamaged.currentHp >= 0) {
    //         HashSet.remove(currentlyOccupiedPoints, bossDamaged.centerCoords)
    //     } else {
    //         Array.append(updatedBosses, bossDamaged)
    //         HashSet.add(currentlyOccupiedPoints, bossDamaged.centerCoords)
    //     }
    // }

    return Model.make({
        ...model,
        eggnemies: updatedEggnemies,
        bosses: updatedBosses,
        occupiedPoints: pipe(
            Array.map(updatedEggnemies, (eggnemy) => eggnemy.centerCoords),
            Array.union(Array.map(updatedBosses, (boss) => boss.centerCoords)),
            HashSet.fromIterable,
        )
        // occupiedPoints: currentlyOccupiedPoints
    })
}

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

function UpdateEggnemyCoords(eggnemies: BadEgg[], playerEggCoords: Point, currentPoints: HashSet.HashSet<Point>,) {
    return CoordUpdateHelper(eggnemies, playerEggCoords, 0, currentPoints, Array.empty())
}

function CoordUpdateHelper(eggnemies: BadEgg[], playerEggCoords: Point, idx: number, 
                            currentPoints: HashSet.HashSet<Point>, ret: BadEgg[]): BadEggsAndPoints {
    if (idx == Array.length(eggnemies)) {
        return BadEggsAndPoints.make({
            eggnemies: pipe(
                ret as Eggnemy[],
                Array.filter((badEgg) => isEggnemy(badEgg))
            ),
            bosses: pipe(
                ret as Boss[],
                Array.filter((badEgg) => isBoss(badEgg))
            ),
            points: currentPoints
        })
    }
    const eggnemy = Array.unsafeGet(eggnemies, idx)
    const eggnemyCoords = pipe(
        eggnemy.centerCoords,
        ({x, y}) => Point.make({x: x, y: y})
    )
    const newPointCandidate = Point.make({
        x:  eggnemyCoords.x < playerEggCoords.x? eggnemyCoords.x + eggnemy.speed :
            eggnemyCoords.x > playerEggCoords.x? eggnemyCoords.x - eggnemy.speed :
            eggnemyCoords.x,
        y:  eggnemyCoords.y < playerEggCoords.y? eggnemyCoords.y + eggnemy.speed :
            eggnemyCoords.y > playerEggCoords.y? eggnemyCoords.y - eggnemy.speed :
            eggnemyCoords.y,    
    })

    const isNewPointOccupied = HashSet.some(currentPoints, 
            ({x, y}) => x == newPointCandidate.x && y == newPointCandidate.y
        )

    // console.log(Equal.equals(Data.struct(eggnemyCoords), Data.struct(eggnemyCoords)))
    const newPoint = !isNewPointOccupied? newPointCandidate : eggnemyCoords
    const newOccupiedPoints = isNewPointOccupied? currentPoints : pipe(
        currentPoints,
        HashSet.filter((coord) => !(coord.x == eggnemyCoords.x && coord.y == eggnemyCoords.y)), // failed to remove, probably due to Point equality
        HashSet.add(newPoint)
    )
    const newEggnemy =  Match.value(eggnemy).pipe(
        Match.tag("Boss", (boss) => Boss.make({
            ...boss,
            centerCoords: newPoint
        })),
        Match.tag("Eggnemy", (eggnemy) =>Eggnemy.make({
            ...eggnemy,
            centerCoords: newPoint
        })),
        Match.exhaustive
    )
    // console.log(newEggnemy)
    const newRet = Array.append(ret, newEggnemy)
    return CoordUpdateHelper(eggnemies, playerEggCoords, idx + 1, newOccupiedPoints, newRet)
}
    
export const update = (msg: Msg, model: Model): Model => 
    Match.value(msg).pipe(
        Match.tag("Canvas.MsgKeyDown", ({ key }) =>
            // pipe(console.log(model), () => false)? model :
            model.gameState != "Ongoing" && key == 'r'? Model.make({
                ...initModel,
                leaderboard: model.leaderboard,
                hasAddedToLeaderboard: false,
            }) :
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
            Model.make({...model, 
                gameState: "PlayerWin",
                leaderboard:    !model.hasAddedToLeaderboard?
                                pipe(
                                    Array.append(model.leaderboard, model.currentTime),
                                    Array.sortBy(
                                        Order.mapInput(Order.number, ({mins, secs}) => mins*60 + secs)
                                    )
                                ):
                                model.leaderboard,
                hasAddedToLeaderboard: true,
            }):
            model.eggnemiesDefeated >= model.eggnemiesToKillBeforeBoss &&
            Array.length(model.bosses) === 0? // Array.isEmptyArray doesnt work for some reason
            spawnBoss(model) :
            model.playerEgg.currentHp <= 0 ? Model.make({
                ...model,
                gameState: "PlayerLose",
            }) :
            model.gameState !== "Ongoing"? model:
            generalUpdate(model)
        ),
        Match.orElse(() => model)
    )

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
        console.log('collision')
        newPlayerHp = Match.value(model.playerEgg.frameCountSinceLastDamaged).pipe(
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
                    )
    } else {
        newPlayerHp = model.playerEgg.currentHp
    }
    console.log(model.gameState)
    return Model.make({
        ...model,
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
        }),
        eggnemies: pipe(
            moveEntities(model.eggnemies, model.playerEgg) as Eggnemy[],
            (eggArr) => randomAddEggnemies(eggArr, 5)
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
