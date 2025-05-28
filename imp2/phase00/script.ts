import { Model, Egg, Point, Settings, EggSides } from "./projectTypes"
import { Array, Schema as S, Match, pipe } from "effect"
import { Cmd, startModelCmd, startSimple } from "cs12242-mvu/src"
import { CanvasMsg, canvasView } from "cs12242-mvu/src/canvas"
import * as Canvas from "cs12242-mvu/src/canvas"
import data from "./settings.json" 

const [PlayerEgg, Eggnemy] = Egg.members

type Msg = typeof CanvasMsg.Type // update strictly only takes in Msg
const update = (msg: Msg, model: Model): Model => 
    Match.value(msg).pipe(
        Match.tag("Canvas.MsgKeyDown", ({ key }) => Model.make({
            ...model,
            playerEgg: PlayerEgg.make({
                ...model.playerEgg,
                centerCoords: stepOnce(key, model.playerEgg.centerCoords, 3)
            })
        })),
        Match.tag('Canvas.MsgTick', () => Model.make({
            ...model,
            currentFrame: (model.currentFrame + 1) % model.fps,
            playerEgg: PlayerEgg.make({
                ...model.playerEgg,
                centerCoords:   !isInBounds(model.playerEgg, 
                                            model.worldWidth, model.worldHeight) ? 
                                returnToBounds( model.playerEgg, 
                                                model.worldWidth, model.worldHeight)! :
                                model.playerEgg.centerCoords,
                current_hp: Array.some(model.eggnemies, (eggnemy) => 
                            isInContact(model.playerEgg, eggnemy)) ? 
                            model.playerEgg.current_hp - 1 : model.playerEgg.current_hp,
            }),
            eggnemies: Array.map(model.eggnemies, (eggnemy) => Eggnemy.make({
                ...eggnemy,
                centerCoords: getNewEggnemyCoords(eggnemy.centerCoords, model.playerEgg.centerCoords, 1)
            }))

        })),
        Match.orElse(() => model)
    )

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
                width: 300,
                height: 300,
                color: "black"
            }),
            ...viewEgg(playerEgg, "white"),
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

    const settings = data as Settings

    const playerEgg = PlayerEgg.make({
        centerCoords: Point.make({
            x: settings.width / 2,
            y: settings.height / 2,
        }),
        height: 20,
        width: 10,
        total_hp: 20,
        current_hp: 20,
        color: "white",
        speed: settings.playerEggSpeed,
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
            })
        ),
        worldHeight: settings.height,
        worldWidth: settings.width,
        fps: settings.fps,
        currentFrame: 0,
    })

    startSimple(root, initModel, update, canvasView(
        settings.width, 
        settings.height,
        settings.fps, 
        "canvas",
        view,
    ))
    // startSimple
}

main()
