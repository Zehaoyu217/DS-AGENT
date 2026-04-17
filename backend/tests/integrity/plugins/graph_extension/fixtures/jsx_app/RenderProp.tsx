import Outer from './Outer'
import Inner from './Inner'

export default function Page() {
  return <Outer render={(x: any) => <Inner x={x} />} />
}
