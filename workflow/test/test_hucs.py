import pytest
import shapely.geometry
import workflow.hucs


from workflow.test.shapes import two_boxes, three_boxes

def test_hc():
    # construction
    things = ['a','b','c','d']
    hc = workflow.hucs.HandledCollection(things)
    assert(len(hc) == 4)
    for i,j in zip(things,hc):
        assert i == j

    # addition
    hc.add('e')
    assert(len(hc) == 5)

    # removal
    hc.pop(3)

    # iteration
    remaining = ['a', 'b', 'c', 'e']
    for i,j in zip(remaining, hc):
        assert i == j

    
def test_hucs(two_boxes):
    # test construction
    tb = workflow.hucs.HUCs(two_boxes)

    # test uniqueness of the boundaries+intersections collections
    handles = [p for b in tb.boundaries for p in b] + [p for i in tb.intersections for p in i]
    assert(len(handles) == 3)
    assert(len(set(handles)) == 3)
    assert(handles == [0,1,2])

    # test correctness of keys
    assert(len(tb.boundaries) == 2)
    assert(list(tb.boundaries.handles()) == [0,1])
    
    assert(len(tb.intersections) == 1)
    assert(list(tb.intersections.handles()) == [0,])

    assert(len(tb.segments) == 3)
    assert(list(tb.segments.handles()) == [0,1,2])

    # gons
    b,i = tb.gons[0]
    assert(list(b) == [0,])
    assert(list(i) == [0,])

    b,i = tb.gons[1]
    assert(list(b) == [1,])
    assert(list(i) == [0,])

    p0 = tb.polygon(0)
    p1 = tb.polygon(1)
    assert(len(p0.boundary.coords) == 5)
    assert(len(p1.boundary.coords) == 5)
    # should check that these are close to those in two_boxes, but
    # they are shifted, so this check would be difficult.
    # for b1,b2 in zip(tb.polygons(), two_boxes):
    #     assert(workflow.utils.close(b1,b2))

    # now split the middle
    # one could imagine iterating over the spine and smoothing/doing something
    for spine in tb.intersections:
        assert(len(spine) is 1)
        int_handle, seg_handle = next(spine.items())
        seg = tb.segments[seg_handle]
        # split seg into two
        assert(len(seg.coords) == 2)
        seg1 = shapely.geometry.LineString([seg.coords[0], (10.,0.)])
        seg2 = shapely.geometry.LineString([(10.,0.), seg.coords[1]])
        tb.segments.pop(seg_handle)
        new_seg_handles = tb.segments.add_many([seg1,seg2])
        spine.pop(int_handle)
        spine.add_many(new_seg_handles)

    # now check that the polygons have 5 coordinates (+1 for repeated start/end)
    p0 = tb.polygon(0)
    p1 = tb.polygon(1)
    assert(len(p0.boundary.coords) == 6)
    assert(len(p1.boundary.coords) == 6)
    print(list(p0.boundary.coords))
    print(list(p1.boundary.coords))


    
    
def test_hucs_three(three_boxes):
    # test construction
    tb = workflow.hucs.HUCs(three_boxes)

    # test uniqueness of the boundaries+intersections collections
    handles = [p for b in tb.boundaries for p in b] + [p for i in tb.intersections for p in i]
    assert(len(handles) == 6)
    assert(len(set(handles)) == 6)
    
    # test correctness of keys
    assert(len(tb.boundaries) == 4)
    assert(len(tb.intersections) == 2)
