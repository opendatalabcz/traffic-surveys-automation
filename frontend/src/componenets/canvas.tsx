import React, { useEffect, useRef, useState } from 'react';

type CanvasProps = {
  imageSrc: string;
};

export const Canvas = (props: CanvasProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);
  const [drawContext, setDrawContext] = useState<CanvasRenderingContext2D>();

  const draw = (event: React.MouseEvent) => {
    updateSize();
    console.log(event);

    if (drawContext) {
      drawContext.beginPath();
      drawContext.moveTo(0, 0);
      drawContext.lineTo(event.clientX, event.clientY);
      drawContext.closePath();
      drawContext.stroke();
    }
  };

  const updateSize = () => {
    if (canvasRef.current && imageRef.current) {
      canvasRef.current.height = imageRef.current.height;
      canvasRef.current.width = imageRef.current.width;
    }
  };

  useEffect(() => {
    const draw = canvasRef.current?.getContext('2d');

    if (draw) {
      console.log('New context');
      draw.lineWidth = 100;
      setDrawContext(draw);
    }
  }, [canvasRef]);

  return (
    <div className="position-relative">
      <img ref={imageRef} src={props.imageSrc} className="position-absolute top-0 start-0 img-fluid" />
      <canvas ref={canvasRef} className="position-absolute top-0 start-0 w-100" onMouseDown={draw}></canvas>
    </div>
  );
};

// $(document).ready(function(){

//   var imageDpi = 300;

//   var can = document.getElementById('canvas');
//   var ctx = can.getContext('2d');
//   var startX, startY;

//   $("canvas").mousedown(function(event){
//       startX = event.pageX;
//       startY= event.pageY;

//       $(this).bind('mousemove', function(e){
//           drawLine(startX, startY, e.pageX, e.pageY);
//       });
//   }).mouseup(function(){
//       $(this).unbind('mousemove');
//   });

//   function drawLine(x, y, stopX, stopY){
//       ctx.clearRect (0, 0, can.width, can.height);
//       ctx.beginPath();
//       ctx.moveTo(x, y);
//       ctx.lineTo(stopX, stopY);
//       ctx.closePath();
//       ctx.stroke();

//       // calculate length
//       var pixelLength = Math.sqrt(Math.pow((stopX - x),2) + Math.pow((stopY-y),2));
//       var physicalLength = pixelLength / imageDpi;
//       console.log("line length = " + physicalLength + " inches (image at " + imageDpi + " dpi)");
//   }
// });
