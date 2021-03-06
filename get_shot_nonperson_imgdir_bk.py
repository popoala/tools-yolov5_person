
import os
import sys
import glob
import numpy as np
import shutil
osp = os.path

shotlabels = ["far","full","human_full","human_upeer","human_face","nonhuman","human_crow"]

labels_add = [0,0,1,2,3,0,1]

def get_nonperson_img(txt_root, img_root, out_dir):
    #import pdb;pdb.set_trace()
    dir_list = os.listdir(img_root)
    dir_list = [ii for ii in dir_list if os.path.isdir(osp.join(img_root, ii))]
    if not osp.exists(out_dir):
        os.makedirs(out_dir)
    ## for each shot_dir
    for dir in dir_list:
        #import pdb;pdb.set_trace()
        dir_path = osp.join(txt_root, dir)
        if not osp.exists(dir_path):
            print(dir_path)
            shotinx = 5
        else:
            ## determin by each img in shot
            txt_list = glob.glob(dir_path+"/*.txt")
            isperson_list = [0]*len(txt_list)
            imglabel_list = []
            # for each img in this shot, save isperson, and get_shot labels
            for txt in txt_list:
                lines = open(txt).readlines()
                w_list = np.array([float(i.strip().split()[3]) for i in lines])
                h_list = np.array([float(i.strip().split()[3]) for i in lines])
                area_list = np.array(w_list) * np.array(h_list)
                max_i = np.argmax(area_list)
                max_w = w_list[max_i]
                max_h = h_list[max_i]
                max_a = area_list[max_i]
                ratio = max_h / max_w if max_h > max_w else max_w/max_h
                if len(lines) > 5:
                    imglabel_list.append(6)  #crow
                elif max_a > 0.2:
                    if ratio < 2:
                        imglabel_list.append(4)  # human_face
                    elif ratio < 4:
                        imglabel_list.append(3)  # human_upper
                    elif ratio < 6:
                        imglabel_list.append(2)  # human_full
                    else:
                        imglabel_list.append(1)  # full
                elif max_a > 0.1:
                    if max_w > 0.7 or max_h > 0.7:
                        if ratio < 2:
                            imglabel_list.append(4)  # human_face, not necessary
                        elif ratio < 4:
                            imglabel_list.append(3)  # human_u
                        elif ratio < 6:
                            imglabel_list.append(2)  # human_full
                        else:
                            imglabel_list.append(1)  # full

                    else:
                        if ratio > 4:
                            imglabel_list.append(1)  # full
                        else:  # maybe cuted
                            print("warning ratio:",txt, max_w, max_h, max_a)
                            imglabel_list.append(1)  # full
                else:
                    print("warning ratio:",txt, max_w, max_h, max_a)
                    imglabel_list.append(1)  # full
            
            img_cnt = len(glob.glob("%s/%s/*.jpg"%(img_root,dir)))
            if len(imglabel_list) < img_cnt:
                imglabel_list.extend([5]*(img_cnt - len(imglabel_list)))
            imglabel_list = np.array(imglabel_list)
            print(txt, imglabel_list)
            counts = np.bincount(imglabel_list)
            sort_inds = counts.argsort()
            if counts[sort_inds[-1]] < counts[sort_inds[-2]]+1:
                print(counts)
                counts = counts+labels_add[:len(counts)]
                print("after weight", counts)
            shotinx = np.argmax(counts)

        if not osp.exists(osp.join(out_dir,shotlabels[shotinx])):
            os.makedirs(osp.join(out_dir,shotlabels[shotinx]))
        shutil.copytree(osp.join(img_root, dir), osp.join(out_dir,shotlabels[shotinx], dir))

            
if __name__ =="__main__":    
    txt_root = sys.argv[1]
    img_root = sys.argv[2]
    out_dir = sys.argv[3]
    get_nonperson_img(txt_root, img_root, out_dir)



