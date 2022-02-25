import { useEffect, useState } from 'react';

type UseImageSizeReturn = {
  imageWidth?: number;
  imageHeight?: number;
  imageRelativeSize?: number;
};

export const useImageSize = (imageRef: HTMLImageElement | null, width?: number): UseImageSizeReturn => {
  const [state, setState] = useState<UseImageSizeReturn>({});

  useEffect(() => {
    if (!imageRef) return;

    setState({
      imageWidth: imageRef.naturalWidth,
      imageHeight: imageRef.naturalHeight,
      imageRelativeSize: width ? imageRef.naturalWidth / width : undefined,
    });
  }, [imageRef, width]);

  return state;
};
