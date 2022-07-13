import nuke
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

def getViewer():
    """Returns the current active viewer node.

    Return:
        obj: The viewer node.
    """
    viewer = nuke.activeViewer()
    if viewer is None:
        logger.error("No active viewer could be found, you need to have a viewer node in the script.")
        return
    return viewer.node()


def getSampleNode():
    """Returns the node to sample that is connected to the current active input of the current viewer.

    Return:
        obj: The sample nuke node.
    """
    viewer = nuke.activeViewer()
    if viewer is None:
        logger.error("No active viewer could be found, you need to have a viewer node in the script.")
        return
    actInput = nuke.ViewerWindow.activeInput(viewer)
    if actInput is None:
        logger.error("No active viewer connection could be found. "
                     "Connect your viewer node to the node you want to sample")
        return
    viewerNode = nuke.activeViewer().node()
    sampleNode = nuke.Node.input(viewerNode, actInput)
    return sampleNode


def getSampleRGBValues(viewerNode, sampleNode):
    """Returns the RGB sample value with the current bbox of the viewer.

    Args:
        viewerNode (object): The active viewer with the bbox to sample.
        sampleNode (object): Nuke node to sample with the given bbox.
    """
    bbox = viewerNode['colour_sample_bbox']
    w = sampleNode.width()
    h = sampleNode.height()
    ratio = float(w) / float(h)

    bboxX = bbox.x()
    bboxY = bbox.y()*ratio

    wd = w / 2
    hd = h / 2

    x = int(round(bboxX * wd + wd))
    y = int(round(bboxY * hd + hd))

    formatWidth = w
    formatHeight = h
    formatAspect = float(formatHeight) / float(formatWidth)

    sampledArea = []
    for index, i in enumerate(bbox.value()):
        if index %2:
            # if width
            coordinate = ((i+1)/2) * formatWidth
        else:
            # if height
            coordinate = (((i/formatAspect) + 1) / 2) * formatHeight
        sampledArea.append(coordinate)

    dx = int(sampledArea[2]-sampledArea[0])
    dy = int(sampledArea[3]-sampledArea[1])

    red = sampleNode.sample("red", x+(dx/2), y+(dy/2), x, y)
    green = sampleNode.sample("green", x+(dx/2), y+(dy/2), x+(dx), y+(dy))
    blue = sampleNode.sample("blue", x+(dx/2), y+(dy/2), x+(dx), y+(dy))

    return red, green, blue


def sampleOnSticky():
    """Function to get the RGB bbox sample value and stored it in a StickyNote."""
    # Get viewer and node to sample
    viewerNode = getViewer()
    if viewerNode is None:
        return
    sampleNode = getSampleNode()
    if sampleNode is None:
        return
    # Get the sample RGB values
    rgbSample = getSampleRGBValues(viewerNode, sampleNode)

    labelText = f"<b>{viewerNode.name()} - {sampleNode.name()}</b>\n" \
                f"<b style=\"color:red;\">R: {round(rgbSample[0], 5):.5f}</b>\n" \
                f"<b style=\"color:green;\">G: {round(rgbSample[1], 5):.5f}</b>\n" \
                f"<b style=\"color:blue;\">B: {round(rgbSample[2], 5):.5f}</b>"
    # Create the stickyNote
    nuke.nodes.StickyNote(label=labelText, note_font_size=40, tile_color=35, note_font_color=15, note_font="arial")

