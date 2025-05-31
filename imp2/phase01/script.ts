import { BadEgg, Boss, Model, Egg, Point, Settings, EggSides,PlayerEgg, Eggnemy, minsSecs } from "./projectTypes"
import { Array, Schema as S, Match, Option, pipe, String } from "effect"
import { Cmd, startModelCmd, startSimple } from "cs12242-mvu/src"
import { CanvasMsg, canvasView } from "cs12242-mvu/src/canvas"
import * as Canvas from "cs12242-mvu/src/canvas"
import data from "./settings.json" 

const settings = data as unknown as Settings // idk why but ts says to convert as unknwon first

type Msg = typeof CanvasMsg.Type // update strictly only takes in Msg
const update = (msg: Msg, model: Model): Model => 
    Match.value(msg).pipe(
        Match.tag("Canvas.MsgKeyDown", ({ key }) =>
            // pipe(console.log(model), () => false)? model :
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
                timeInSeconds: Math.floor(model.currentFrame / model.fps),
                currentFrame: model.currentFrame + 1,
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
                timeInSeconds: Math.floor(model.currentFrame / model.fps),
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

const getTimer = (frameCount: number, fps: number): string =>
    pipe(
        frameCount / fps,
        Math.floor,
        (secs) => minsSecs.make({
            mins: Math.floor(secs / 60),
            secs: secs % 60
        }),
        ({mins, secs}) =>   `${pipe(`${mins}`, String.padStart(2, "0"))}` + ':' +
                            `${pipe(`${secs}`, String.padStart(2, "0"))}`
    )

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

// const moveEgg = (egg: Egg) =>
//     Match.value(egg).pipe(
//         Match.tag("Eggnemy", (eggnemy) => Eggnemy.make({
            
//         }))
//     )

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
    
// const isInBounds = (egg: Egg, width: number, height: number): boolean => 
//     getSideBoundary(egg, "left") < 0 ||
//     getSideBoundary(egg, "right") > width ||
//     getSideBoundary(egg, "top") < 0 || 
//     getSideBoundary(egg, "bottom") > height ?
//     false : true

const returnPlayerToBounds = (model: Model): Model =>
    Model.make({
        ...model,
        worldCenter: (
            getSideBoundary(model.playerEgg, 'right')
            >= (model.worldCenter.x + model.worldWidth / 2) ?
            // to right   
            Point.make({...model.worldCenter, 
                        x: model.playerEgg.centerCoords.x - model.worldWidth / 2 
                        + model.playerEgg.width / 2
                    }) :
            getSideBoundary(model.playerEgg, 'left')
            <= (model.worldCenter.x - model.worldWidth / 2) ?
            Point.make({...model.worldCenter, 
                        x: model.playerEgg.centerCoords.x + model.worldWidth / 2  
                        - model.playerEgg.width / 2
                    }) :
            getSideBoundary(model.playerEgg, 'top')
            <= (model.worldCenter.y - model.worldHeight / 2) ?
            Point.make({...model.worldCenter, 
                        y: model.playerEgg.centerCoords.y + model.worldHeight / 2  
                        - model.playerEgg.height / 2
                    }) :
            getSideBoundary(model.playerEgg, 'bottom') 
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


const getSideBoundary = (egg: Egg, side: EggSides) =>
    side == "bottom" ? egg.centerCoords.y + egg.height / 2 :
    side == "top" ? egg.centerCoords.y - egg.height / 2 :
    side == "left" ? egg.centerCoords.x - egg.width / 2 :
    egg.centerCoords.x + egg.width / 2


const view = (model: Model) => 
    pipe(
        model,
        ({ playerEgg, eggnemies, bosses }) => [
            Canvas.Clear.make({
                color: "black",
            }),
            Canvas.OutlinedRectangle.make({
                x: model.worldCenter.x - (model.worldWidth / 2),
                y: model.worldCenter.y - (model.worldHeight / 2), 
                width: model.worldWidth,
                height: model.worldHeight,
                color: "white",
                lineWidth: model.worldBoundaryWidth,
            }),
            ...pipe(
                Array.map(bosses, (boss) => viewEgg(boss, boss.color)),
                Array.flatten
            ),
            ...pipe(
                Array.map(eggnemies, (eggnemy) => viewEgg(eggnemy, "grey")),
                Array.flatten
            ),
            ...(model.gameState == "PlayerLose"? Array.empty(): viewEgg(playerEgg, "white")), // spread empty array
            Canvas.Text.make({
                x: 50,
                y: 50,
                text: `${model.eggnemiesDefeated}`,
                fontSize: 30,
                color: "white",
            }),
            model.gameState === "PlayerWin"? Canvas.Text.make({
                x: getSideBoundary(model.playerEgg, "left") - 10,
                y: getSideBoundary(model.playerEgg, "top") - 20,
                text: "You win!",
                color: "white",
                fontSize: 20,
            }): Canvas.NullElement.make({}),
            Canvas.Text.make({
                x: settings.screenWidth - 150,
                y: 50,
                text: getTimer(model.currentFrame, model.fps),
                color: "white",
                fontSize: 20,
            })
        ],

    )

const viewEgg = (egg: Egg , color: string) => 
    [
        Canvas.SolidRectangle.make({
                    x: egg.centerCoords.x - (egg.width / 2),
                    y: egg.centerCoords.y - (egg.height / 2),
                    width: egg.width,
                    height: egg.height,
                    color: color,
        }),
        Canvas.Text.make({
            x: egg.centerCoords.x - egg.width,
            y: getSideBoundary(egg, "bottom") + 10,
            text: `${egg.currentHp}/${egg.totalHp}`,
            color: egg.color,
            fontSize: 12,
        })
    ]

    

const getNewEggnemyCoords = (eggnemyCoords: Point, playerEggCoords: Point, eggnemySpeed: number): Point => 
    Point.make({
        x:  eggnemyCoords.x < playerEggCoords.x? eggnemyCoords.x + eggnemySpeed :
            eggnemyCoords.x > playerEggCoords.x? eggnemyCoords.x - eggnemySpeed :
            eggnemyCoords.x,
        y:  eggnemyCoords.y < playerEggCoords.y? eggnemyCoords.y + eggnemySpeed :
            eggnemyCoords.y > playerEggCoords.y? eggnemyCoords.y - eggnemySpeed :
            eggnemyCoords.y,
    })


function main() {
    const root = document.getElementById("root")!

    const playerEgg = PlayerEgg.make({
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

    const initModel = Model.make({
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
        timeInSeconds: 0,
        gameState: "Ongoing",
    })

    startSimple(root, initModel, update, canvasView(
        settings.screenWidth, 
        settings.screenHeight,
        settings.fps, 
        "canvas",
        view,
    ))
    // startSimple
}

main()

// const stepOnce = (key: string, pointFrom: Point, stepLength: number): Point =>
//     Point.make({
//         x:  key == "d"? pointFrom.x + stepLength :
//             key == "a"? pointFrom.x - stepLength :
//             pointFrom.x,
//         y:  key == "s"? pointFrom.y + stepLength :
//             key == "w"? pointFrom.y - stepLength :
//             pointFrom.y,
//     })

// const viewEgg = (egg: Egg , color: string) => 
    
//     Match.value(egg).pipe(
//         Match.tag('PlayerEgg', (playerEgg) => [
//         Canvas.SolidRectangle.make({
//                     x: playerEgg.centerCoords.x - (playerEgg.width / 2),
//                     y: playerEgg.centerCoords.y - (playerEgg.height / 2),
//                     width: playerEgg.width,
//                     height: playerEgg.height,
//                     color: color,
//         }),
//         Canvas.Text.make({
//             x: playerEgg.centerCoords.x - playerEgg.width,
//             y: getSideBoundary(playerEgg, "bottom") + 10,
//             text: `${playerEgg.currentHp}/${playerEgg.totalHp}`,
//             color: playerEgg.color,
//             fontSize: 12,
//         })
//     ]),
//     Match.tag("Eggnemy", (eggnemy) => [
//         Canvas.SolidRectangle.make({
//             x: eggnemy.centerCoords.x - (eggnemy.width / 2),
//             y: eggnemy.centerCoords.y - (eggnemy.height / 2),
//             width: eggnemy.width,
//             height:eggnemy.height,
//             color: color,
//         }),
//         Canvas.Text.make({
//             x: eggnemy.centerCoords.x - eggnemy.width,
//             y: getSideBoundary(eggnemy, "bottom") + 10,
//             text: `${eggnemy.currentHp}/${eggnemy.totalHp}`,
//             color: eggnemy.color,
//             fontSize: 12,
//         })
//     ]),
//     Match.exhaustive
//     )

// const moveWordBorderRelativeToPlayer = (model: Model, key: string) =>
//     Model.make({
//         ...model,
//         worldCenter: moveRelativeToPlayer(
//                     model.worldCenter,
//                     String.toLowerCase(key),
//                     model.playerEgg.speed,
//                 )
//     })
