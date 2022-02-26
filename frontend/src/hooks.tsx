import { useEffect, useState } from 'react';
import { TaskClient } from './api/task';
import { TaskConfiguration } from './types';

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

export const useTaskConfiguration = () => {
  const taskClient = new TaskClient();

  const [state, setState] = useState<TaskConfiguration>({});

  useEffect(() => {
    taskClient.getConfiguration().then(config => setState(config));
  }, []);

  return state;
};
