import { Model, Egg, EggSides, Point } from "./projectTypes"
import { Array, Schema as S, Match, pipe } from "effect"
import { Cmd, startModelCmd, startSimple } from "cs12242-mvu/src"
import { CanvasMsg, canvasView } from "cs12242-mvu/src/canvas"
import * as Canvas from "cs12242-mvu/src/canvas"

const playerEgg = Egg.make({
    centerCoords: Point.make({
        x: 0,
        y: 0,
    }),
    height: 20,
    width: 10,
    total_hp: 20,
    current_hp: 20
})

const initModel = Model.make({
    playerEgg: playerEgg,
    eggnemies: Array.empty(),
    worldHeight: 300,
    worldWidth: 300,
    fps: 60,
    currentFrame: 0,
})

type Msg = typeof CanvasMsg.Type // update strictly only takes in Msg
const update = (msg: Msg, model: Model): Model => 
    Match.value(msg).pipe(
        Match.tag("Canvas.MsgKeyDown", ({ key }) => Model.make({
            ...model,
            playerEgg: Egg.make({
                ...model.playerEgg,
                centerCoords: stepOnce(key, model.playerEgg.centerCoords, 1)
            })
        })),
        Match.tag('Canvas.MsgTick', () => Model.make({
            ...model,
            currentFrame: (model.currentFrame + 1) % model.fps,
            playerEgg: Egg.make({
                ...model.playerEgg,
                centerCoords:   !isInBounds(model.playerEgg, 
                                            model.worldWidth, model.worldHeight) ? 
                                returnToBounds( model.playerEgg, 
                                                model.worldWidth, model.worldHeight)! :
                                model.playerEgg.centerCoords
            })

        })),
        Match.orElse(() => model)
    )

const isInBounds = (egg: Egg, width: number, height: number) => 
    getSideBoundary(egg, "left") < 0 ||
    getSideBoundary(egg, "right") > width ||
    getSideBoundary(egg, "top") < 0 || 
    getSideBoundary(egg, "bottom") > height ?
    false : true

const returnToBounds = (egg: Egg, width: number, height: number): Point | null =>
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
            viewEgg(model.playerEgg, "white"),
            ...Array.map(model.eggnemies, (eggnemy) => viewEgg(eggnemy, "grey"))
        ]
    )

const viewEgg = (egg: Egg, color: string) => 
    Canvas.SolidRectangle.make({
                x: egg.centerCoords.x - (egg.width / 2),
                y: egg.centerCoords.y - (egg.height / 2),
                width: egg.width,
                height: egg.height,
                color: color,
    })

const root = document.getElementById("root")!

startSimple(root, initModel, update, canvasView(
    300, 
    300,
    30, 
    "canvas",
    view,
))
// startSimple