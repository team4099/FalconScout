import React from "react"
import { useEffect, useState } from "react"
import ReactDOM from 'react-dom';
import { render } from "react-dom";
import { ComponentSetup } from "../interface"

interface TimerState {
  running: Boolean,
  currentTime: number
}

export class Timer extends React.Component<ComponentSetup, TimerState> {
    watch: NodeJS.Timeout | undefined;

    constructor(props: ComponentSetup){
        super(props)

        this.state = {
            running: false,
            currentTime: 0,
          };
    
    }

    start = () => {
        if (!this.state.running) {
            this.setState({ running: true });
            this.watch = setInterval(() => this.pace(), 100);
        }
    };

    stop = () => {
        this.setState({ running: false });
        clearInterval(this.watch);
    };

    pace = () => {
        this.setState({ currentTime: this.state.currentTime + 0.1 });
    };

    reset = () => {
        this.setState({
            currentTime: 0,
        });
    };

    render() {
        return (
            <div className="mx-3 my-3 mt-3">
                <label className="block text-[#344054] text-sm mb-2">
                    {this.props.text}
                </label>
                <div className="flex flex-row gap-2">
                    <div className="basis-1/2 h-[8.5rem] border-2 border-gray-200 rounded-xl">
                        <h1 className="text-xl mt-4 text-center font-semibold">Stopwatch</h1>
                        <h1 className="text-4xl mt-4 text-center font-bold">{this.state.currentTime.toFixed(1)}</h1>
                    </div>
                    <div className="basis-1/2 h-[8.5rem]">
                        {this.state.running == false && (
                            <button className="h-[4rem] w-full border-2 bg-[#c0c7d5] text-[#29313c] rounded-xl text-lg text-center font-semibold" onClick={this.start}>
                                Start
                            </button>
                        )}
                        {this.state.running == true && (
                            <button className="h-[4rem] w-full border-2 bg-[#c0c7d5] text-[#29313c] rounded-xl text-lg text-center font-semibold" onClick={this.stop}>
                                Stop
                            </button>
                        )}
                        <button className="h-[4rem] w-full mt-[0.5rem] border-2 bg-[#3b4858] text-[#d7e3f8] rounded-xl text-lg text-center font-semibold" onClick={this.reset}>
                            Reset
                        </button>
                    </div>
                </div>
            </div>
        )
    }
}