import { Model, Egg, Point } from "./projectTypes"
import { Array, Schema as S, Match, pipe } from "effect"
import { Cmd, startModelCmd, startSimple } from "cs12242-mvu/src"
import { CanvasMsg, canvasView } from "cs12242-mvu/src/canvas"
import * as Canvas from "cs12242-mvu/src/canvas"

const playerEgg = Egg.make({
    centerCoords: Point.make({
        x: 0,
        y: 0
    }),
    height: 20,
    width: 10,
    total_hp: 20,
    current_hp: 20
})

const initModel = Model.make({
    playerEgg: playerEgg,
    eggnemies: Array.empty(),
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
            currentFrame: (model.currentFrame + 1) % model.fps
        })),
        Match.orElse(() => model)
    )

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
            Canvas.SolidRectangle.make({
                x: playerEgg.centerCoords.x,
                y: playerEgg.centerCoords.y,
                width: playerEgg.width,
                height: playerEgg.height,
                color: "white",
            }),
            ...Array.map(model.eggnemies, (eggnemy) => viewEgg(eggnemy, "white"))
        ]
    )

const viewEgg = (egg: Egg, color: string) => 
    Canvas.SolidRectangle.make({
                x: egg.centerCoords.x,
                y: egg.centerCoords.y,
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