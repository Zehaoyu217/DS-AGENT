import { lazy } from 'react'

const Heavy = lazy(() => import('./Heavy'))

export default function Page() {
  return <Heavy />
}
