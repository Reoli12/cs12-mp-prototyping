import { Point } from './projectTypes'
import { Array, Equal, Data , HashSet, pipe } from 'effect'

const mySet = HashSet.empty()

const testPoint = Point.make({x: 1, y: 1})

const mySet2 = HashSet.add(mySet, Data.struct(testPoint))
const mySet3 = HashSet.add(mySet2, Data.struct(testPoint))

console.log(pipe(
    mySet3,
    Array.fromIterable,
))