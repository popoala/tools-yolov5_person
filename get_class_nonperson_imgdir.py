
import os
import sys
import glob
import numpy as np
import shutil
osp = os.path

shotlabels = ["far","full","human_full","human_upeer","human_face","nonhuman","human_crow"]
badlabels = [2,3,4,6]

## img of label 2 3 & 4 is not kept
def get_nonperson_class(txt_root, img_root, out_dir):
    #import pdb;pdb.set_trace()
    dir_list = os.listdir(img_root)
    dir_list = [ii for ii in dir_list if os.path.isdir(osp.join(img_root, ii))]
    if not osp.exists(out_dir):
        os.makedirs(out_dir)
    ## for each shot_dir
    for dir in dir_list:
        #import pdb;pdb.set_trace()
        dir_path = osp.join(txt_root, dir)
        ## no human
        if not osp.exists(dir_path):
            print(dir_path)
            shotinx = 5
            if not osp.exists(osp.join(out_dir)):
                os.makedirs(osp.join(out_dir))
            shutil.copytree(osp.join(img_root, dir), osp.join(out_dir,dir))
        else:
            this_dir = osp.join(out_dir,dir)
            thisimg_dir = osp.join(img_root,dir)
            imgname_list = os.listdir(thisimg_dir)
            imgname_list = [ii.replace(".jpg","") for ii in imgname_list if ii.endswith(".jpg")]
            #import pdb;pdb.set_trace()
            ## determin each img in shot
            txt_list = glob.glob(dir_path+"/*.txt")
            txtname_list = [osp.basename(ii).replace(".txt","") for ii in txt_list if ii.endswith(".txt")]
            imglabel_list = []
            # for each img in this shot
            for imgname in imgname_list:
                if imgname not in txtname_list:
                    if not osp.exists(this_dir):
                        os.makedirs(this_dir)
                    shutil.copy(osp.join(thisimg_dir, imgname+".jpg"), osp.join(this_dir, imgname+".jpg"))
                    continue

                txt = txt_list[txtname_list.index(imgname)]
                lines = open(txt).readlines()
                w_list = np.array([float(i.strip().split()[3]) for i in lines])
                h_list = np.array([float(i.strip().split()[3]) for i in lines])
                area_list = np.array(w_list) * np.array(h_list)
                max_i = np.argmax(area_list)
                max_w = w_list[max_i]
                max_h = h_list[max_i]
                max_a = area_list[max_i]
                ratio = max_h / max_w if max_h > max_w else max_w/max_h
                
                ## get determine label
                if len(lines) > 5 and max_a<0.2:
                    imglabel_list.append(6)  #crow
                elif max_a >= 0.2:
                    if ratio < 2:
                        imglabel_list.append(4)  # human_face
                    elif ratio < 4:
                        imglabel_list.append(3)  # human_upper
                    elif ratio < 6:
                        imglabel_list.append(2)  # human_full
                    else:
                        imglabel_list.append(1)  # full
                elif max_a > 0.05:
                    if max_w > 0.1 or max_h > 0.1:
                        if ratio < 2:
                            imglabel_list.append(4)  # human_face, not necessary
                        elif ratio < 4:
                            imglabel_list.append(3)  # human_u
                        elif ratio < 6:
                            imglabel_list.append(2)  # human_full
                        else:
                            imglabel_list.append(1)  # full

                    else:
                        print("warning ratio:",txt, max_w, max_h, max_a)
                        if ratio < 3:
                            imglabel_list.append(3)  # full
                        elif ratio < 6:  # maybe cuted
                            imglabel_list.append(2)  # human_full
                        else:
                            imglabel_list.append(1)  # full
                else:
                    print("warning ratio:",txt, max_w, max_h, max_a)
                    imglabel_list.append(1)  # full
                
                #print(imgname,txt, len(lines), imglabel_list[-1])
                ## save image
                if imglabel_list[-1] in badlabels:
                    #print("droping ",imgname)
                    continue
                else:
                    if not osp.exists(this_dir):
                        os.makedirs(this_dir)
                    print("save ",imgname, txt, len(lines), imglabel_list[-1])
                    shutil.copy(osp.join(thisimg_dir, imgname+".jpg"), osp.join(this_dir, imgname+".jpg"))
        

            
if __name__ =="__main__":    
    txt_root = sys.argv[1]
    img_root = sys.argv[2]
    out_dir = sys.argv[3]
    get_nonperson_class(txt_root, img_root, out_dir)



