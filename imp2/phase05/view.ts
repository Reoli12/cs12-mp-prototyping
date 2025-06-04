import { Array, Match, Option, pipe, String } from 'effect'
import { Model } from "./model"
import * as Canvas from "cs12242-mvu/src/canvas"
import { settings, Egg, EggUtils, minsSecs, Point } from "./projectTypes"
import { value } from 'effect/Redacted'

export const view = (model: Model) => 
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
                x: EggUtils.left(model.playerEgg) - 10,
                y: EggUtils.top(model.playerEgg) - 20,
                text: "You win!",
                color: "white",
                fontSize: 20,
            }): Canvas.NullElement.make({}),
            model.gameState == "PlayerLose" || model.gameState == "PlayerWin" ? 
            showRestartPrompt(model) : Canvas.NullElement.make({}),
            Canvas.Text.make({
                x: settings.screenWidth - 150,
                y: 50,
                text: getTimer(model.currentTime),
                color: "white",
                fontSize: 20,
            }),
            ...printRowHelper(
                Array.make("Top 1", "2", "3"), 
                settings.screenWidth / 6, 
                (settings.screenHeight * (8/10)),
                30, 0, Array.empty()
            ),
            ...printRow(model.leaderboard, 
                (settings.screenWidth / 6) + 100, 
                (settings.screenHeight * (8/10)),
                30),
            ...printRowHelper(
                Array.make("Atk", "Spd", "Exp"), 
                settings.screenHeight * (9/10), 
                (settings.screenHeight * (8/10)),
                30, 0, Array.empty()
            ),
            ...printRowHelper(
                Array.make( `${model.playerEgg.attack}`, 
                            `${model.playerEgg.speed}`, 
                            `${model.playerEgg.eggxperience}`), 
                settings.screenHeight * (9.5/10), 
                (settings.screenHeight * (8/10)),
                30, 0, Array.empty()
            ),
            ...(model.gameState === "ChoosingEgghancement" ? 
            showEgghancementPrompt(
                model,
                Point.make({
                    y: model.screenHeight / 2,
                    x: model.screenWidth / 2
                }),
                model.worldWidth,
                model.worldHeight / 2,
                ) :
            Array.make(Canvas.NullElement.make({})))
        ],
    )

const showEgghancementPrompt = (model : Model, center: Point, width: number, height: number) => Array.make(
    Canvas.SolidRectangle.make({
        x: center.x - width/2,
        y: center.y - width/2,
        width: width,
        height: height,
        color: "black"
    }),
    Canvas.OutlinedRectangle.make({
        x: center.x - width/2,
        y: center.y - height/2,
        width: width,
        height: height,
        color: "white",
        lineWidth : model.worldBoundaryWidth
    }),
    ...printRowHelper(
        Array.make(
            `[1] Increase max HP by ${model.deltaHp}`,
            `[2] Increase attack by ${model.deltaAttack}`,
            `[3] Increase speed by ${model.deltaSpeed}`
        ),
        center.x + width/ 4,
        center.y - height/ 4,
        20,
        0,
        Array.empty()
    )
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
            y: EggUtils.bottom(egg) + 10,
            text: `${egg.currentHp}/${egg.totalHp}`,
            color: egg.color,
            fontSize: 12,
        })
    ]

const getTimer = (time: minsSecs): string =>
    pipe(
        time,
        ({mins, secs}) =>   `${pipe(`${mins}`, String.padStart(2, "0"))}` + ':' +
                            `${pipe(`${secs}`, String.padStart(2, "0"))}`
        )

const showRestartPrompt = (model: Model) =>
    Canvas.Text.make({
        x: EggUtils.left(model.playerEgg) - 20,
        y: model.playerEgg.centerCoords.y + 2* model.playerEgg.height,
        text: "Restart? (R)",
        fontSize: 12,
        color: "white"
    })

const printRow = (leaderboard: readonly minsSecs[], x: number, y: number, fontSize: number) =>
    pipe(
        // leaderboard,
        Array.map(leaderboard, (time) => getTimer(time)),
        (arr) => Array.pad(arr, 3, '-:--'),
        (arr) => printRowHelper(arr, x, y, fontSize, 0, Array.empty())
    )

function printRowHelper(toDisplay: string[], x: number, y: number, fontSize: number, idx: number, 
                                res: (typeof Canvas.Text.Type)[]) {
    if (idx == 3) {
        return res
    }

    const newLine = Canvas.Text.make({
        x: x,
        y: y + fontSize*(idx + 1),
        text: Array.unsafeGet(toDisplay, idx),
        color: "white",
        fontSize: fontSize,
        textAlign: "right"
    })

    return printRowHelper(toDisplay, x, y, fontSize, idx + 1,
        Array.append(res, newLine)
    )
}


