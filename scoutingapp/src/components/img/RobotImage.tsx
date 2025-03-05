import React, {useEffect, useState} from "react"
import { ComponentSetup } from "../interface"

export const emptyImage = <img
    style={{height: "0px", alignItems: 'center', justifyContent: 'center', margin: "auto"}}
    src={`./src/components/img/gray.png`}
/>

export function RobotImage(props: ComponentSetup) {
  const [componentInside, setComponentInside] = useState(<></>)
  const robotNumber = props.getValue["TeamNumber"]

  useEffect(() => {
    const interval = setInterval(() => {
      if (robotNumber) {
        fileExists(`./src/components/img/${robotNumber}.jpeg`).then((exists) => {
          console.log("Exists => ", exists)
          if (exists) {
            setComponentInside(
                <img
                    style={{ height: "300px", alignItems: 'center', justifyContent: 'center', margin: "auto"}}
                    src={`./src/components/img/${robotNumber}.jpeg`}
                />
            )
          } else {
            setComponentInside(
                <img
                    style={{ height: "0px", alignItems: 'center', justifyContent: 'center', margin: "auto"}}
                    src={`./src/components/img/gray.png`}
                />
            )
          }
        });
      } else {
        setComponentInside(
          <img
            style={{ height: "0px", alignItems: 'center', justifyContent: 'center', margin: "auto"}}
            src={`./src/components/img/gray.png`}
          />
        )
      }
    }, 500)
    return () => clearInterval(interval);
  })

  return (<>
    {componentInside}
  </>)
}

async function fileExists(imagePath: string): Promise<boolean> {
  try {
    const response = await fetch(imagePath, { method: "HEAD" });
    return response.ok;
  } catch {
    return false;
  }
}