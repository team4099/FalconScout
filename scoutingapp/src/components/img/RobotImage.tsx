import React from "react"
import { ComponentSetup } from "../interface"

interface RobotImageProps extends ComponentSetup {
  robotNumber?: string;
}

export const emptyImage = <img
  style={{width: "80%", height: "80%", alignItems: 'center', justifyContent: 'center'}}
  src='../img/gray.png'
  alt={`Picture of robot`}
/>

export function RobotImage({ robotNumber = "4099", ...props }: RobotImageProps) {
  return (
    <img
      style={{ width: "60%", height: "60%", alignItems: 'center', justifyContent: 'center', margin: "auto"}}
      src={`./src/components/img/${robotNumber}.png`}
      alt={`Picture of robot ${robotNumber}`}
    />
  )
}