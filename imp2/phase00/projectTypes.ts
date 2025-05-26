import { Schema as S } from 'effect'

export const Point = S.Struct({
    x: S.Number,
    y: S.Number,
})
export type Point= typeof Point.Type

export const Egg = S.Struct({
    center: Point,
})
export type Egg = typeof Egg.Type

export const Model = S.Struct({
    playerEgg: Egg,
    eggnemies: S.Array(Egg),
    })
export type Model = typeof Model.Type