CUDA_VISIBLE_DEVICES=2 python main.py --storepath testing-config1-model-poisson-uncover --model dense \
                                    --modelpath dense-15t9-15h46-r5-zoom1 --rewardfunc ver5 \
                                    --zoom 1 --poisson true --testing true --usingmodel true --mapwidth 50 \
                                    --mapheight 400 --uncover 5 --generation 8 --coverrange 10 \
                                     --clambda 0.01 --velocity 10

CUDA_VISIBLE_DEVICES=2 python main.py --storepath testing-config2-model-poisson-uncover --model dense \
                                    --modelpath dense-15t9-15h46-r5-zoom1 --rewardfunc ver5 \
                                    --zoom 1 --poisson true --testing true --usingmodel true --mapwidth 50 \
                                    --mapheight 400 --uncover 10 --generation 8 --coverrange 10 \
                                     --clambda 0.01 --velocity 10

CUDA_VISIBLE_DEVICES=2 python main.py --storepath testing-config3-model-poisson-uncover --model dense \
                                    --modelpath dense-15t9-15h46-r5-zoom1 --rewardfunc ver5 \
                                    --zoom 1 --poisson true --testing true --usingmodel true --mapwidth 50 \
                                    --mapheight 400 --uncover 15 --generation 8 --coverrange 10 \
                                     --clambda 0.01 --velocity 10 

CUDA_VISIBLE_DEVICES=2 python main.py --storepath testing-config4-model-poisson-uncover --model dense \
                                    --modelpath dense-15t9-15h46-r5-zoom1 --rewardfunc ver5 \
                                    --zoom 1 --poisson true --testing true --usingmodel true --mapwidth 50 \
                                    --mapheight 400 --uncover 20 --generation 8 --coverrange 10 \
                                     --clambda 0.01 --velocity 10

CUDA_VISIBLE_DEVICES=2 python main.py --storepath testing-config5-model-poisson-uncover --model dense \
                                    --modelpath dense-15t9-15h46-r5-zoom1 --rewardfunc ver5 \
                                    --zoom 1 --poisson true --testing true --usingmodel true --mapwidth 50 \
                                    --mapheight 400 --uncover 25 --generation 8 --coverrange 10 \
                                     --clambda 0.01 --velocity 10 

CUDA_VISIBLE_DEVICES=2 python main.py --storepath testing-config6-model-poisson-uncover --model dense \
                                    --modelpath dense-15t9-15h46-r5-zoom1 --rewardfunc ver5 \
                                    --zoom 1 --poisson true --testing true --usingmodel true --mapwidth 50 \
                                    --mapheight 400 --uncover 30 --generation 8 --coverrange 10 \
                                     --clambda 0.01 --velocity 10