import { startSimple } from 'cs12242-mvu/src'
import { settings } from "./projectTypes"
import { initModel } from "./model"
import { view } from "./view"
import { update } from "./update"
import { canvasView } from 'cs12242-mvu/src/canvas'

function main() {
    const root = document.getElementById("root")!

    startSimple(root, initModel, update, canvasView(
    settings.screenWidth, 
    settings.screenHeight,
    settings.fps, 
    "canvas",
    view,
))
}

main()