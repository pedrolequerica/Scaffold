import { DebugContracts } from "./_components/DebugContracts";
import type { NextPage } from "next";
import { getMetadata } from "~~/utils/scaffold-eth/getMetadata";

export const metadata = getMetadata({
  title: "Green Goblin Bot",
  description: "Green Goblin Bot",
});

const Debug: NextPage = () => {
  return (
    <>
      <DebugContracts />
      <div className="text-center mt-8 bg-secondary p-10">
        <h1 className="text-4xl my-0">Green Goblin Bot</h1>
        <br></br>
        <br></br>
        <br></br>
        <code className="text-center mt-8 bg-secondary p-10">
          <th>
            <tr>Swap</tr>
            <tr>Raw Price</tr>
            <tr>Raw Price Src</tr>
            <tr>O Price - incl. Slippage Adj.</tr>
            <tr>Timestamp - local time</tr>
          </th>
          <th>
            <tr>BTC/USD</tr>
            <tr>60000</tr>
            <tr>Uniswap</tr>
            <tr>60008</tr>
            <tr>09:30:00</tr>
          </th>
        </code>{" "}
      </div>
    </>
  );
};

export default Debug;
