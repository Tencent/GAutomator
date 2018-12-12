"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""

__author__ = 'yifengcai'

import time
import os
import operator
import re
import sys
import random
import traceback

import wpyscripts.manager as manager
from wpyscripts.tools.traverse.layerelem import TouchElem, ViewLayer
from wpyscripts.tools.traverse.graph import Graph, dijkstra
from wpyscripts.tools import baisc_operater as tools
from wpyscripts.tools.traverse import qqwx

logger = manager.get_logger()
engine = manager.get_engine()
device = manager.get_device()
reporter=manager.get_reporter()

# globals
game_package = ""
game_activity = ""

seen_elements = set()
clicked_elements = set()
visited_layer = set()
unclick_element_2_layers = {}     # TouchElement -> ViewLayer set
layer_2_unclick_cnt = {}        # ViewLayer -> int

desuffix_dict = {}      # desuffixed tuple -> [elements' name]
desuffix_filter_names = []   # elements' name

click_dict_ex = {}



def find_less_click_element_ex(elements):
    '''
    @summary: this version wants to fix a bug in NBA "chat" layer: 3 buttons share the same path, so the latter 2 will never be clicked
    now I record all the elements that are least clicked and have same path, and choose random one
    '''
    global click_dict_ex
    min_num = sys.maxint
    min_elements = []
    min_poses = []
    min_object_name = None
    num = 0
    for e, pos in elements:
        if click_dict_ex.has_key(e.object_name):
            num = click_dict_ex[e.object_name]
        else:
            num = 0
            click_dict_ex.setdefault(e.object_name, 0)
            
        if num < min_num:
            min_elements = [e]
            min_poses = [pos]
            min_object_name = e.object_name
            min_num = num
        elif num == min_num and min_object_name == e.object_name:
            min_elements.append(e)
            min_poses.append(pos)
            
    logger.info("chose less click element %s, num is %d", min_object_name, min_num)
    click_dict_ex[min_object_name] = min_num + 1
    aint = random.randint(0, len(min_elements)-1)
    return min_elements[aint], min_poses[aint]



def clear_view_layer_in_global(view_layer):
    global unclick_element_2_layers, layer_2_unclick_cnt
    
    for elem in unclick_element_2_layers:
        if view_layer in unclick_element_2_layers[elem]:
            unclick_element_2_layers[elem].remove(view_layer)
            
    if view_layer in layer_2_unclick_cnt:
        del layer_2_unclick_cnt[view_layer]


def init_game_activity():
    global game_package, game_activity
    
    package_activity = device.get_top_package_activity()
    game_package, game_activity = package_activity.package_name, package_activity.activity
    logger.info("Game package and activity is (%s, %s)", game_package, game_activity)

def in_game_activity():
    '''
    @return: bool value
    '''
    package_activity = device.get_top_package_activity()    
    if package_activity is None or package_activity.package_name != game_package or package_activity.activity != game_activity:
        if package_activity:
            logger.debug("package name is %s, activity is %s", package_activity.package_name, package_activity.activity)
        else:
            logger.debug("package_activity is %s", package_activity)
        return False
    else:
        return True


def click_screen_center():
    display_size = device.get_display_size()
    if display_size:
        width, height = display_size.width, display_size.height
        engine.click_position(width*0.5, height*0.5)
    else:
        logger.warn("can not get display size, click screen corner")
        click_screen_corner()
        
def click_screen_corner():
    engine.click_position(10, 10)


def desuffix_objname(name):
    '''
    @summary: de-suffix numbers in last three object name parts
    @note: "/ViewUIDepth_2/Canvas5/Chat4/Panel3/JumpWindow2/InputField1" -> '/ViewUIDepth_2/Canvas5/Chat4/Panel/JumpWindow/InputField'
    '''
    return re.sub(r"(/.*/\D+)\d*(/\D+)\d*(/\D+)\d*", r"\1\2\3", name)

def get_desuffixed_elements(elements, thres=30):
    global desuffix_dict, desuffix_filter_names
    ret = []
    
    for elem in elements:
        objname = elem[0].object_name
        desuffixed_objname = desuffix_objname(objname)
        
        desuffix_dict.setdefault(desuffixed_objname, [])
        
        if objname in desuffix_dict[desuffixed_objname]:
            ret.append(elem)
        else:
            if len(desuffix_dict[desuffixed_objname]) >= thres:
                if objname not in desuffix_filter_names:
                    desuffix_filter_names.append(objname)
                    logger.info("element desuffix full, filter it: %s", objname)
            else:
                desuffix_dict[desuffixed_objname].append(objname)
                ret.append(elem)
        
    return ret

def log_desuffix():
    logger.debug("desuffix filtered name cnt: %d, they are:\n%s", len(desuffix_filter_names), "\n".join(desuffix_filter_names))



def find_in_screen_elements(elements):
    display_size = device.get_display_size()
    if not display_size:
        return elements

    ret = []
    width, height = display_size.width, display_size.height
    
    for elem in elements:
        _, pos = elem
        if 0 <= pos["x"] <= width and 0 <= pos["y"] <= height:
            ret.append(elem)
        else:
            logger.warn("element not in screen: %s", elem)
    
    return ret



def find_unseen_elements(elements, scene_name):
    unseen_elements = []
    
    for elem in elements:
        e = TouchElem(scene_name, elem[0])
        if e not in seen_elements:
            unseen_elements.append(elem)
    
    return unseen_elements

def find_seen_but_unclick_elements(elements, scene_name):
    unclick_elements = []
    
    for elem in elements:
        e = TouchElem(scene_name, elem[0])
        if e not in clicked_elements:
            unclick_elements.append(elem)
    
    return unclick_elements


def get_layer_sorted_by_unclick():
    layers = sorted(layer_2_unclick_cnt.items(), key=operator.itemgetter(1), reverse=True)
    layers = filter(lambda x: x[1] != 0, layers)
    
    return layers

def find_max_layer_unclick_reachable(graph, start):
    '''
    @return: (end ViewLayer, a ViewLayer path from start to end)
    @attention: return value may be (None, None) if no more unclick layer
    '''
    layers = get_layer_sorted_by_unclick()
    
    end = None
    path = None
    for end, num in layers:
        logger.info("try a max unclick layer: %s, unclick cnt: %d", end, num)
        
        start_vertex = graph.get_vertex(start)
        end_vertex = graph.get_vertex(end)
        
        path = dijkstra(graph, start_vertex, end_vertex)
        if path:
            logger.info("find a path is:\n%s", "\n".join([str(p) for p in path]))
            break
        else:
            logger.info("no reachable path to view_layer: %s, re-choose another", end)
            continue
    else:
        logger.info("no more unclick layer")
    
    return end, path
        
def go_through_graph_path(graph, path, forbid_names):
    '''
    @return: (prev layer, prev entry, click number)
    '''
    prev_layer = None
    prev_entry = None
        
    # go through the path
    num = 0
    for i in range(0, len(path)-1):
        time.sleep(3)
        
        from_vertex = graph.get_vertex(path[i])
        to_vertex = graph.get_vertex(path[i+1])
        
        # get current real layer
        elements = engine.get_touchable_elements()
        if forbid_names:
            elements = [e for e in elements if e[0].object_name not in forbid_names]
        elements = find_in_screen_elements(elements)
        scene_name = engine.get_scene()
        elements = get_desuffixed_elements(elements)
        curr_layer = ViewLayer()
        for e, _ in elements:
            te = TouchElem(scene_name, e)
            curr_layer.add_element(te)
        curr_layer.sort_elems_by_name()
        
        # current layer diff from memory
        if curr_layer != path[i]:
            if i > 0:
                logger.info("layer in real not equal to layer in memory, need to reset the edge")
                prev_layer = path[i-1]
                prev_entry = graph.get_vertex(path[i-1]).get_entry(from_vertex)
                
                graph.del_edge(path[i-1], path[i])
            else:
                logger.warn("layer path[0] in real not equal to layer in memory, impossible?!")
                
            break
        else:
            logger.info("layer in real match memory, good")
            
        edge_element = from_vertex.get_entry(to_vertex)
        elem = engine.find_element(edge_element.element.object_name)
        
        if elem:
            tools.screen_shot_click(elem)
            num += 1
            logger.info("go through path from %s to %s, edge is %s", path[i], path[i+1], edge_element)
        else:
            logger.info("no entry %s in layer %s, clear the edge", edge_element, path[i])
            graph.del_edge(path[i], path[i+1])
            break
    else:
        # last layer in path
        time.sleep(3)
        
        # get current real layer
        elements = engine.get_touchable_elements()
        if forbid_names:
            elements = [e for e in elements if e[0].object_name not in forbid_names]
        elements = find_in_screen_elements(elements)
        scene_name = engine.get_scene()
        elements = get_desuffixed_elements(elements)
        curr_layer = ViewLayer()
        for e, _ in elements:
            te = TouchElem(scene_name, e)
            curr_layer.add_element(te)
        curr_layer.sort_elems_by_name()
        
        if curr_layer != path[-1]:
            if len(path) > 1:
                logger.info("layer in real not equal to layer in memory, need to reset the edge")
                prev_layer = path[-2]
                prev_entry = graph.get_vertex(path[-2]).get_entry(graph.get_vertex(path[-1]))
                
                graph.del_edge(path[-2], path[-1])
            else:
                logger.warn("layer path[0] in real not equal to layer in memory, impossible?!")
            
        else:
            logger.info("layer in real match memory, good")
        
    return (prev_layer, prev_entry, num)


stat_dict = {}      # {cnt number: (clicked number, seen number, visited layer cnt)}
def count_stat(cnt, clicked, seen, layercnt):
    global stat_dict
    
    if cnt in stat_dict:
        if stat_dict[cnt] != (clicked, seen, layercnt):
            logger.warn("stat number in cnt %d differs", cnt)
            
        return
    
    stat_dict[cnt] = (clicked, seen, layercnt)
    
def output_stat(filename):
    # filename is abs
    logger.info("output stat in file: %s", filename)
    
    maxcnt = 0
    curr_index = 0
    
    for cnt in stat_dict:
        if cnt > maxcnt:
            maxcnt = cnt
        
    with open(filename, "w") as fout:    
        for i in range(maxcnt+1):
            if i in stat_dict:
                curr_index = i
            else:
                logger.info("use old index %d in loop %d", curr_index, i)
                
            fout.write("%d,%d,%d,%d\n" % (i, stat_dict[curr_index][0], stat_dict[curr_index][1], stat_dict[curr_index][2]))     
    

def explore(statfilename = "policy.log", forbid_names=None, mode=0, max_num=300, interval=3):
    # mode: 0 for new strategy, 1 for old one
    
    global seen_elements, clicked_elements, visited_layer, unclick_element_2_layers, layer_2_unclick_cnt
    policy_cnt = [0, 0, 0, 0]
    
    logger.info("Start Exploring")
    
    graph = Graph()
    
    init_game_activity()
    
    prev_layer = None
    prev_entry = None
    
    cnt = 0
    error=0
    not_in_game = False
    while cnt < max_num:
        time.sleep(interval)
        count_stat(cnt, len(clicked_elements), len(seen_elements), len(visited_layer))
        logger.info("loop cnt is %d", cnt)
        
        # not game package, sleep some time first to make it stable
        if not in_game_activity():
            time.sleep(10)
        
        if not in_game_activity():
            if qqwx.check_qq_wx_package():
                # try to handle qq/wx package
                qqwx.handle_qq_wx_package()
            elif not_in_game:
                logger.info("not game package anymore, raise Exception")
                raise Exception, "not game package anymore"
            else:
                # exit this layer
                logger.info("not game package, back")
                device.back()
                prev_layer = None
                prev_entry = None
                cnt += 1
                not_in_game = True
                continue
        not_in_game = False

        elements=[]
        try:
            elements = engine.get_touchable_elements()
        except:
            elements=None
            stack=traceback.format_exc()
            not_in_game=True
            logger.warn(stack)
            reporter.screenshot()
        
        # get elements timed out (0 fps)
        if elements is None:
            logger.info("get elements timed out, back")
            if qqwx.check_qq_wx_package():
                # try to handle qq/wx package
                qqwx.handle_qq_wx_package()
            else:
                # exit this layer
                logger.info("not game package, back")
                device.back()
            prev_layer = None
            prev_entry = None
            cnt += 1
            continue
        
        if forbid_names:
            elements = [e for e in elements if e[0].object_name not in forbid_names]
        elements = find_in_screen_elements(elements)
        scene_name = engine.get_scene()
        elements = get_desuffixed_elements(elements)
        # no touchable element
        if len(elements) == 0:
#             logger.info("no touchable element, click screen center")
#             click_screen_center()
            logger.info("no touchable element, click screen corner")
            click_screen_corner()
            prev_layer = None
            prev_entry = None
            cnt += 1
            continue
        
        unseen_elements = find_unseen_elements(elements, scene_name)
        unclick_elements = find_seen_but_unclick_elements(elements, scene_name)
        
        # set current layer
        curr_layer = ViewLayer()
        for e, _ in elements:
            te = TouchElem(scene_name, e)
            curr_layer.add_element(te)
        curr_layer.sort_elems_by_name()
#         logger.info("current layer data:\n%s", curr_layer.fullstr())
        logger.info("current layer: %s", curr_layer)
        
        # add vertex
        if not graph.check_vertex(curr_layer):
            graph.add_vertex(curr_layer)
        
        if curr_layer not in visited_layer:
            visited_layer.add(curr_layer)
            
        # set globals
        clear_view_layer_in_global(curr_layer)
        layer_2_unclick_cnt[curr_layer] = 0
        
        for e, _ in elements:
            te = TouchElem(scene_name, e)
            
            # add TouchElement into seen_elements
            if te not in seen_elements:
                seen_elements.add(te)
                
            # if this is an unclick element
            if te not in clicked_elements:
                # if this unclick element was not recorded before
                if te not in unclick_element_2_layers or curr_layer not in unclick_element_2_layers[te]:
                    layer_2_unclick_cnt[curr_layer] += 1
                    
                    # add into unclick_element_2_layers
                    unclick_element_2_layers.setdefault(te, set()).add(curr_layer)
                    
        # add edge
        if prev_layer and prev_entry:
            graph.add_edge(prev_layer, curr_layer, prev_entry)
        else:
            logger.info("prev layer and entry are None, ignore the edge")
        
        
        if mode == 1:
            # old strategy
            e, pos = tools.find_less_click_element(elements)
        else:
            # new strategy
            if unseen_elements:
                e, pos = unseen_elements[0]
                logger.info("choose an unseen element: %s", e.object_name)
                policy_cnt[0] += 1
            elif unclick_elements:
                e, pos = unclick_elements[0]
                logger.info("choose an unclick element: %s", e.object_name)
                policy_cnt[1] += 1
            else:
                # check if current layer has only 1 element and no edge out
                # NOTE!!! this policy is very *TRICKY* and should be fixed in SDK engine later
                outlayers =  [l.id for l in graph.get_vertex(curr_layer).get_connections()]
                if len(elements) == 1 and (not outlayers or (len(outlayers) == 1 and outlayers[0] == curr_layer)):
                    logger.info("only 1 element and no edge to other layer, click screen corner")
                    click_screen_corner()
                    prev_layer = None
                    prev_entry = None
                    cnt += 1
                    continue
                
                logger.info("current layer contains no unclick element")
                max_unclick_layer, path = find_max_layer_unclick_reachable(graph, curr_layer)
                if max_unclick_layer and path:
                    logger.info("choose a max unclick layer: %s", max_unclick_layer)
                    prev_layer, prev_entry, num = go_through_graph_path(graph, path, forbid_names)
                    cnt += num
                    logger.info("cnt adds %d", num)
                    policy_cnt[2] += 1
                    continue
                else:
                    rand = random.randint(0, len(elements))
                    logger.info("choose an action by random: %d", rand)
                    if rand == 0:
                        # this policy could possibly combine with *no edge out* policy
                        # say: delete *no edge out* policy, and only use this one
                        logger.info("click screen corner")
                        click_screen_corner()
                        prev_layer = None
                        prev_entry = None
                        cnt += 1
                        continue
                    else:
                        e, pos = find_less_click_element_ex(elements)
                        logger.info("choose a less click one: %s", e.object_name)
                        policy_cnt[3] += 1
        
        # actually click the element
        tools.screen_shot_click_pos(pos["x"], pos["y"])
        
        # handle new click element
        te = TouchElem(scene_name, e)
        if te not in clicked_elements:
            logger.info("handle new click element: %s", te)
            
            # add into clicked_elements
            clicked_elements.add(te)
            
            # count down all related layers
            if te in unclick_element_2_layers:
                for layer in unclick_element_2_layers[te]:
                    layer_2_unclick_cnt[layer] -= 1
                    
                    # protect the code
                    if layer_2_unclick_cnt[layer] < 0:
                        logger.warn("layer_2_unclick_cnt[layer] negative, must be wrong. %s", layer)
                        layer_2_unclick_cnt[layer] = 0
                    
                # delete TouchElem from unclick_element_2_layers
                del unclick_element_2_layers[te]
        
        # set prev layer and entry
        prev_layer = curr_layer
        prev_entry = te
        
        # add loop count
        cnt += 1
        
    count_stat(cnt, len(clicked_elements), len(seen_elements), len(visited_layer))
        
    logger.info("Finish Exploring")
    output_stat(statfilename)
    
    logger.debug("%s", graph)
    log_desuffix()
    
    seen_sum = len(seen_elements)
    clicked_sum = len(clicked_elements)
    unclick_sum = 0
    unclick_sum_zero = 0
    for k in unclick_element_2_layers:
        if len(unclick_element_2_layers[k]) > 0:
            unclick_sum += 1
        else:
            unclick_sum_zero += 1
    logger.info("sumcheck. seen sum: %d, clicked sum: %s, unclick sum: %s, unclick sum zero: %s", seen_sum, clicked_sum, unclick_sum, unclick_sum_zero)
    
    logger.info("visited layer cnt: %d", len(visited_layer))
    logger.info("each policy cnt: %s", policy_cnt)
    
    sum1 = 0
    for v in graph:
        sum1 += layer_2_unclick_cnt[v.get_id()]
    sum2 = 0
    for elem in unclick_element_2_layers:
        sum2 += len(unclick_element_2_layers[elem])
    logger.info("sumcheck. layer sum unclick cnt is %d, unclick element sum layer is %d", sum1, sum2)
    
    for elem in unclick_element_2_layers:
        logger.debug("unclick element contained in following layers: %s", elem)
        for layer in unclick_element_2_layers[elem]:
#             logger.debug("%s", layer.fullstr())
            logger.debug("%s", layer)
