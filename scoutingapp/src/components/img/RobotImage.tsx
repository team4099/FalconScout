import React, {useEffect, useState} from "react"
import { ComponentSetup } from "../interface"

export function RobotImage(props: ComponentSetup) {
  const [componentInside, setComponentInside] = useState(<></>)
  const robotNumber = props.getValue["TeamNumber"]

  useEffect(() => {
    if (robotNumber) {
      fileExists(`../${robotNumber}.jpeg`).then((exists) => {
        if (exists) {
          setComponentInside(
            <img
              style={{height: "300px", alignItems: 'center', justifyContent: 'center', margin: "auto"}}
              src={`../${robotNumber}.jpeg`}
              alt={''}
            />
          )
          return
        }
      })
    }

    setComponentInside(
      <></>
    )
  }, [robotNumber])

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