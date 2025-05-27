import { Model, Egg, Point } from "./projectTypes"
import { Array, Schema as S, Match } from "effect"
import { Cmd, startModelCmd } from "cs12242-mvu/src"
import { CanvasMsg, canvasView } from "cs12242-mvu/src/canvas"

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

const update = (msg: CanvasMsg, model: Model) => 
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
        }))
    )

const stepOnce = (key: string, pointFrom: Point, stepLength: number): Point =>
    Point.make({
        x:  key == "d"? pointFrom.x + stepLength :
            key == "a"? pointFrom.x - stepLength :
            pointFrom.x,
        y:  key == "s"? pointFrom.y + stepLength :
            key == "w"? pointFrom.y - stepLength :
            pointFrom.x,
    })