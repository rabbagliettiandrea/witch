from invoke import Collection, Program

from witch import VERSION
from .tasks import dev, prod, utils

namespace = Collection()
namespace.add_collection(prod)
namespace.add_collection(dev)
namespace.add_collection(utils)
namespace.add_task(prod.deploy)

program = Program(namespace=namespace, version=VERSION)
