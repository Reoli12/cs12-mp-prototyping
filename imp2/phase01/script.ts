import { Model, Egg, Point, Settings, EggSides,PlayerEgg, Eggnemy } from "./projectTypes"
import { Array, Schema as S, Match, Option, pipe } from "effect"
import { Cmd, startModelCmd, startSimple } from "cs12242-mvu/src"
import { CanvasMsg, canvasView } from "cs12242-mvu/src/canvas"
import * as Canvas from "cs12242-mvu/src/canvas"
import data from "./settings.json" 

type Msg = typeof CanvasMsg.Type // update strictly only takes in Msg
const update = (msg: Msg, model: Model): Model => 
    Match.value(msg).pipe(
        Match.tag("Canvas.MsgKeyDown", ({ key }) =>
            // pipe(console.log(model), () => false)? model :
            model.isOver? model : 
            (key == 'l' || key == 'L') ? 
            modelDefeatedEggnemies(model) :
            Model.make({
            ...model,
            playerEgg: PlayerEgg.make({
                ...model.playerEgg,
                centerCoords: stepOnce(key, model.playerEgg.centerCoords, 3),
            })
        })),
        Match.tag('Canvas.MsgTick', () => 
            model.playerEgg.current_hp <= 0 ? Model.make({
                ...model,
                isOver: true,
            }) :
            model.isOver? model :
            Array.some(model.eggnemies, (eggnemy) => isInContact(model.playerEgg, eggnemy)) ? Model.make({
                // with collision
                ...model,
                currentFrame: (model.currentFrame + 1) % model.fps,
                playerEgg: PlayerEgg.make({
                    ...model.playerEgg,
                    centerCoords:   handleBoundsBehavior( model.playerEgg,
                                                        model.worldWidth,
                                                        model.worldHeight
                    ),
                    current_hp: Match.value(model.playerEgg.frameCountSinceLastDamaged).pipe(
                        Match.tag("None", () => model.playerEgg.current_hp),
                            // if we decrement immediately after a new collision, the next tick will
                            // decrement as well, leading to a double decrement
                        Match.tag("Some", (frameCountSinceLastDamaged) => (
                            // if more than one frame has passed since last dmg, decrement 1
                            frameCountSinceLastDamaged.value < model.fps? 
                            model.playerEgg.current_hp : model.playerEgg.current_hp - 1
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
            eggnemies: Array.map(model.eggnemies, (eggnemy) => Eggnemy.make({
                ...eggnemy,
                centerCoords: getNewEggnemyCoords(eggnemy.centerCoords, model.playerEgg.centerCoords, 1)
            })),
            }) : Model.make({
                // no collision 
                ...model,
                playerEgg: PlayerEgg.make({
                    ...model.playerEgg,
                    centerCoords: handleBoundsBehavior( model.playerEgg,
                                                        model.worldWidth,
                                                        model.worldHeight
                    ),
                    frameCountSinceLastDamaged: Match.value(model.playerEgg.frameCountSinceLastDamaged).pipe(
                        Match.tag("None", () => Option.none()),
                        Match.tag("Some", (frameCount) => 
                            frameCount.value < model.fps? Option.some(frameCount.value + 1) :
                            Option.none()
                    ),
                    Match.exhaustive
                )
                }),
                    eggnemies: Array.map(model.eggnemies, (eggnemy) => Eggnemy.make({
                        ...eggnemy,
                        centerCoords: getNewEggnemyCoords(eggnemy.centerCoords, model.playerEgg.centerCoords, 1)
                })),
                
            }),
        ),
        Match.orElse(() => model)
    )

const modelDefeatedEggnemies = (model: Model): Model => 
    Model.make({
        ...model,
        eggnemies: Array.filter(model.eggnemies, 
            (eggnemy) => withinPlayerRange(model.playerEgg, eggnemy))
    }) 

const withinPlayerRange = (player: PlayerEgg, eggnemy: Eggnemy): boolean =>
    // no specific definition as to what range was given
    (player.attackRange ** 2) >= 
    (player.centerCoords.x - eggnemy.centerCoords.x) ** 2 + 
    (player.centerCoords.y - eggnemy.centerCoords.y) ** 2 

const handleBoundsBehavior = (egg: Egg, width: number, height: number): Point =>
    !isInBounds(egg, width, height) ? 
    returnToBounds( egg, width, height)! :
    egg.centerCoords

const absDifference = (a: number, b: number): number =>
    Math.abs(a - b)

const isInContact = (egg1: Egg, egg2: Egg): boolean => 
    absDifference(egg1.centerCoords.x, egg2.centerCoords.x) < (egg1.width + egg2.width) / 2 &&
    absDifference(egg1.centerCoords.y, egg2.centerCoords.y) < (egg1.height + egg2.height) / 2
    
const isInBounds = (egg: Egg, width: number, height: number) => 
    getSideBoundary(egg, "left") < 0 ||
    getSideBoundary(egg, "right") > width ||
    getSideBoundary(egg, "top") < 0 || 
    getSideBoundary(egg, "bottom") > height ?
    false : true

const returnToBounds = (egg: Egg, width: number, height: number): Point | null =>
    // maybe better to use tagged structs
    getSideBoundary(egg, "left") < 0 ? Point.make({...egg.centerCoords, x: egg.width / 2}) :
    getSideBoundary(egg, "right") > width ? Point.make({...egg.centerCoords, x: width - egg.width / 2}) :
    getSideBoundary(egg, "top") < 0 ? Point.make({...egg.centerCoords, y: egg.height / 2}) :
    getSideBoundary(egg, "bottom") > height ? Point.make({...egg.centerCoords, y: height - egg.height / 2}) :
    null

const getSideBoundary = (egg: Egg, side: EggSides) =>
    side == "bottom" ? egg.centerCoords.y + egg.height / 2 :
    side == "top" ? egg.centerCoords.y - egg.height / 2 :
    side == "left" ? egg.centerCoords.x - egg.width / 2 :
    egg.centerCoords.x + egg.width / 2

const stepOnce = (key: string, pointFrom: Point, stepLength: number): Point =>
    Point.make({
        x:  key == "d"? pointFrom.x + stepLength :
            key == "a"? pointFrom.x - stepLength :
            pointFrom.x,
        y:  key == "s"? pointFrom.y + stepLength :
            key == "w"? pointFrom.y - stepLength :
            pointFrom.y,
    })

const view = (model: Model) => 
    pipe(
        model,
        ({ playerEgg, eggnemies }) => [
            Canvas.SolidRectangle.make({
                x: 0,
                y: 0,
                width: model.screenWidth,
                height: model.screenHeight,
                color: "black",
            }),
            Canvas.OutlinedRectangle.make({
                x: 0,
                y: 0, 
                width: model.worldWidth,
                height: model.worldHeight,
                color: "white",
                lineWidth: 3,
            }),
            ...(model.isOver? Array.empty(): viewEgg(playerEgg, "white")), // spread empty array
            ...pipe(
                Array.map(eggnemies, (eggnemy) => viewEgg(eggnemy, "grey")),
                Array.flatten
            ),
        ],

    )

const viewEgg = (egg: Egg , color: string) => 
    Match.value(egg).pipe(
        Match.tag('PlayerEgg', (playerEgg) => [
        Canvas.SolidRectangle.make({
                    x: playerEgg.centerCoords.x - (playerEgg.width / 2),
                    y: playerEgg.centerCoords.y - (playerEgg.height / 2),
                    width: playerEgg.width,
                    height: playerEgg.height,
                    color: color,
        }),
        Canvas.Text.make({
            x: playerEgg.centerCoords.x - playerEgg.width,
            y: getSideBoundary(playerEgg, "bottom") + 10,
            text: `${playerEgg.current_hp}/${playerEgg.total_hp}`,
            color: playerEgg.color,
            fontSize: 12,
        })
    ]),
    Match.tag("Eggnemy", (eggnemy) => [
        Canvas.SolidRectangle.make({
            x: eggnemy.centerCoords.x - (eggnemy.width / 2),
            y: eggnemy.centerCoords.y - (eggnemy.height / 2),
            width: eggnemy.width,
            height:eggnemy.height,
            color: color,
        }),
    ]),
    Match.exhaustive
    )
    

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

    const settings = data as unknown as Settings // idk why but ts says to convert as unknwon first

    const playerEgg = PlayerEgg.make({
        centerCoords: Point.make({
            x: settings.worldWidth / 2,
            y: settings.worldHeight / 2,
        }),
        height: 20,
        width: 10,
        total_hp: 20,
        current_hp: 20,
        color: "white",
        speed: settings.playerEggSpeed,
        attackRange: settings.playerEggRange,
        frameCountSinceLastDamaged: Option.none()
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
            }),
            // Eggnemy.make({
            //     centerCoords: Point.make({x: 100, y: 250}),
            //     height: settings.eggnemyHeight,
            //     width: settings.eggnemyWidth,
            //     color: "gray",
            //     speed: settings.eggnemySpeed,
            // }),
            // Eggnemy.make({
            //     centerCoords: Point.make({x: 200, y: 200}),
            //     height: settings.eggnemyHeight,
            //     width: settings.eggnemyWidth,
            //     color: "gray",
            //     speed: settings.eggnemySpeed,
            // }),
        ),
        worldHeight: settings.worldHeight,
        worldWidth: settings.worldWidth,
        screenHeight: settings.screenHeight,
        screenWidth: settings.screenWidth,
        fps: settings.fps,
        currentFrame: 0,
        isOver: false,
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