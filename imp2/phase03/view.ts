import { Array, Match, Option, pipe, String } from 'effect'
import { Model } from "./model"
import * as Canvas from "cs12242-mvu/src/canvas"
import { settings, Egg, EggUtils, minsSecs } from "./projectTypes"
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
            model.gameState != "Ongoing"? showRestartPrompt(model) : Canvas.NullElement.make({}),
            Canvas.Text.make({
                x: settings.screenWidth - 150,
                y: 50,
                text: getTimer(model.currentTime),
                color: "white",
                fontSize: 20,
            }),
            ...showLeaderboard(model.leaderboard, 30)
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

const showLeaderboard = (leaderboard: readonly minsSecs[], fontSize: number) =>
    pipe(
        // leaderboard,
        Array.map(leaderboard, (time) => getTimer(time)),
        (arr) => Array.pad(arr, 3, '--:--'),
        (arr) => showLeaderboardHelper(arr, fontSize, 0, Array.empty())
    )

function showLeaderboardHelper(toDisplay: string[], fontSize: number, idx: number, 
                                res: (typeof Canvas.Text.Type)[]) {
    if (idx == 3) {
        return res
    }

    const newLine = Canvas.Text.make({
        x: settings.screenWidth / 10,
        y: settings.screenHeight * 8/10 + fontSize*(idx + 1),
        text: Array.unsafeGet(toDisplay, idx),
        color: "white",
        fontSize: fontSize
    })

    return showLeaderboardHelper(toDisplay, fontSize, idx + 1,
        Array.append(res, newLine)
    )
}


