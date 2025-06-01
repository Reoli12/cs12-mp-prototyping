import { Array, pipe, String } from 'effect'
import { Model } from "./model"
import * as Canvas from "cs12242-mvu/src/canvas"
import { settings, Egg, EggUtils, minsSecs } from "./projectTypes"

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
            Canvas.Text.make({
                x: settings.screenWidth - 150,
                y: 50,
                text: getTimer(model.currentTime),
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